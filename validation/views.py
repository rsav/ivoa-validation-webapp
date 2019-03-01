from django.shortcuts import render
from django.views.generic.list import ListView, View, BaseListView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from .models import Services, Errors
from .forms import ServicesListForm, ServersListForm, ErrorsListForm, EfreqsListForm, DEFAULT_SVC_TYPE, DEFAULT_SVC_DATE_MIN
from django.views.generic.edit import FormView, BaseFormView
import logging
from datetime import date
from urllib.parse import urlparse
from django.db.models import Count,Sum,Func,F
from django.views.generic.edit import FormMixin
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import urllib
import html


#from multi_form_view import MultiFormView # I tried multi_form_view to add a second form, but did not work (complex inheritance?)
#import six

logger = logging.getLogger('validation')

# URLs of validators for each spec (as in the services.spec column)
VALIDATOR_BASE_URLS={
     "Simple Cone Search"           : "http://voparis-validator.obspm.fr/validator.php?"
    ,"Simple Image Access"          : "http://voparis-validator.obspm.fr/validator.php?"
    ,"Simple Spectral Access"       : "http://voparis-validator.obspm.fr/validator.php?"
    ,"Table Access Protocol"        : "http://voparis-validation.obspm.fr/tapvalidator.php?"
}


class CustomListView(FormView, ListView): # inheriting from FormMixin enough here ?


    # cf https://stackoverflow.com/questions/52275218/how-to-access-session-variable-inside-form-class
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs      
  
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        #context['form'] = ServicesListForm(request=self.request)
        
        # hum, not sure why we need those, but else some errors are found in a bootstrap4 template and the query is made several times (with LIMIT 21)
        context['tag']=False # cf https://stackoverflow.com/questions/23223443/how-can-extra-context-be-passed-to-django-crispy-forms-field-templates/41189096
        context['wrapper_class']='Dummy'
        return context    
    




class ServersListView(CustomListView): 
    template_name = 'validation/servers.html'
    form_class = ServersListForm 
    success_url = 'servers'
    model = Services
    
    #paginate_by = 25
    def form_valid(self, form):
        logger.info('ServersListView.form_valid self.request.POST.get=%s',self.request.POST.get)
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # get posted data                 
        type = form.cleaned_data['type'] 
        date_min = form.cleaned_data['date_min']

        if self.request.POST.get('display',False): # button display was clicked

            logger.info('ServersListView.form_valid: form received: new type=%s new date_min=%s' % (type,date_min))
    
            # put these data in session vars
            self.request.session['svc_type'] = type 
            self.request.session['svc_date_min'] = str(date_min) 
    
            return super().form_valid(form)

        if self.request.POST.get('services',False): # button errors was clicked
            
            # extract server from posted data
            server = form.cleaned_data['server']

            logger.info('ServersListView.form_valid: servers-form received: server=%s' % server)
            
            # Redirect to services page for this server
            return redirect(reverse('services')+"?svc_server="+server)
        
        if self.request.POST.get('efreqs',False): # button errors frequency was clicked
            
            # extract server from posted data
            server = form.cleaned_data['server']

            logger.info('ServersListView.form_valid: efreqs-form received: server=%s' % server)
            
            # Redirect to errors frequency page for this service
            return redirect(reverse('efreqs')+"?svc_server="+server)        
    
    def get_queryset(self):
        svc_type = self.request.session.get('svc_type',DEFAULT_SVC_TYPE) # get svc_type from session var where we put it or its default value
        svc_date_min = self.request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # get svc_date_min from session var or its default value of today      
        
        # this makes a GROUP BY query: cf https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html
        # => SELECT "services"."url", COUNT("services"."ivoid") AS "nb_ivoid", SUM("services"."nb_warn") AS "nb_warn", SUM("services"."nb_err") AS "nb_err", SUM("services"."nb_fatal") AS "nb_fatal", SUM("services"."nb_fail") AS "nb_fail" FROM "services" WHERE ("services"."date" >= '2019-01-15' AND "services"."svc_type" = 'TAP') GROUP BY "services"."url" ORDER BY "nb_ivoid" DESC
        # in addition we use the server_from_url function declared on the PosgreSQL server to extract hostname:port from the URL
        servers = Services.objects.filter(svc_type=svc_type,date__gte=svc_date_min).values(name=Func(F('url'), function='server_from_url')).annotate(
                                                                                                            nb_ivoid=Count('ivoid'),
                                                                                                            nb_warn=Sum('nb_warn'),
                                                                                                            nb_err=Sum('nb_err'),
                                                                                                            nb_fatal=Sum('nb_fatal'),
                                                                                                            nb_fail=Sum('nb_fail'),
                                                                                                            ).order_by('-nb_ivoid')
        
        return servers
        
        

class EfreqsListView(CustomListView): 
    template_name = 'validation/efreqs.html'
    form_class = EfreqsListForm 
    success_url = 'efreqs'
    model = Errors
    
    #paginate_by = 25
    
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Transmit this GET variable to template
        context['svc_server'] = self.request.GET.get('svc_server',None) 
        return context
    
    
    
    def form_valid(self, form):
        logger.info('EfreqsListView.form_valid self.request.POST.get=%s',self.request.POST.get)
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # get posted data                 
        type = form.cleaned_data['type'] 
        date_min = form.cleaned_data['date_min']


        logger.info('EfreqsListView.form_valid: form received: new type=%s new date_min=%s' % (type,date_min))

        # put these data in session vars
        self.request.session['svc_type'] = type 
        self.request.session['svc_date_min'] = str(date_min) 

        return super().form_valid(form)
   
    
    def get_queryset(self):
        logger.info('EfreqsListView.get_queryset: ')
        
        svc_type = self.request.session.get('svc_type',DEFAULT_SVC_TYPE) # get svc_type from session var where we put it or its default value
        svc_date_min = self.request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # get svc_date_min from session var or its default value of today      
        
        # this makes a GROUP BY query: cf https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html
        # => SELECT "services"."url", COUNT("services"."ivoid") AS "nb_ivoid", SUM("services"."nb_warn") AS "nb_warn", SUM("services"."nb_err") AS "nb_err", SUM("services"."nb_fatal") AS "nb_fatal", SUM("services"."nb_fail") AS "nb_fail" FROM "services" WHERE ("services"."date" >= '2019-01-15' AND "services"."svc_type" = 'TAP') GROUP BY "services"."url" ORDER BY "nb_ivoid" DESC
        # in addition we use the server_from_url function declared on the PosgreSQL server to extract hostname:port from the URL
        errors = Errors.objects.filter(svc_type=svc_type,date__gte=svc_date_min).values('name','type').annotate(count=Count('name')).order_by('-count')
        
        svc_server = self.request.GET.get('svc_server',False)
        if svc_server:
            
            logger.info('EfreqsListView.get_queryset: got svc_server=%s' % svc_server)
            errors = errors.filter(url__icontains=svc_server)
        
        return errors
        
        

    
class ServicesListView(CustomListView): 
    template_name = 'validation/services.html'
    form_class = ServicesListForm
    success_url = 'services'
    model = Services
     
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Transmit these GET variables to template
        context['svc_server'] = self.request.GET.get('svc_server',None) 
        return context
    
    
    def form_valid(self, form):
        logger.info('ServicesListView.form_valid')
        #logger.info(self.request.POST)
        
        
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
         
         
        type = form.cleaned_data['type'] 
        date_min = form.cleaned_data['date_min']
        #display = form.cleaned_data['display']
        #validate = form.cleaned_data['validate']
        
        if self.request.POST.get('validate',False): # button validate was clicked
        
            # get data posted
            ivoid = form.cleaned_data['ivoid']
            url = form.cleaned_data['url']
            params = form.cleaned_data['params']
            spec = form.cleaned_data['spec']
            specv = form.cleaned_data['specv']
            
            
            
            # Transform &amp; to & etc.
            params = html.unescape(params)
            
            logger.info('ServicesListView.form_valid: validate-form received: ivoid=%s url=%s params=%s specv=%s' % (ivoid,url,params,specv))
            
            
            # Create validator URL
            vurl = VALIDATOR_BASE_URLS[spec]  
            
            vurl += params
            # add spec and spec version
            vurl += "&"+urllib.parse.urlencode({"spec":spec+" "+specv})
            # add service URL
            vurl += "&"+urllib.parse.urlencode({"serviceURL":url})  
              
            if(spec=="Table Access Protocol"): # TAP validator also needs the timeout
                vurl += "&"+urllib.parse.urlencode({"timeout":600})
                vurl += "&"+urllib.parse.urlencode({"maxtable":"1"}) # added reduce time taken by TAP validation (it will check only one table)
          
              
            logger.info('ServicesListView.form_valid: Redirecting to vurl=%s',vurl)
              
            # Redirect to validator page (the template makes sure that it will appear in another tab)
            return HttpResponseRedirect(vurl)
        
        if self.request.POST.get('display',False): # button display was clicked
            
            logger.info('ServicesListView.form_valid: display-form received: new type=%s new date_min=%s' % (type,date_min))
    
            self.request.session['svc_type'] = type # put svc_type in session var
            self.request.session['svc_date_min'] = str(date_min) # put svc_date_min in session var

            return super().form_valid(form)

        if self.request.POST.get('errors',False): # button errors was clicked
            
            # extract ivoid and url from posted data
            ivoid = form.cleaned_data['ivoid']
            url = form.cleaned_data['url']
            url = html.unescape(url) # coming from HTML this contains &amp; => change to &
            
            logger.info('ServicesListView.form_valid: errors-form received: ivoid=%s url=%s' % (ivoid,url))
             
            url = urllib.parse.quote(url) # quote before sending in URL - necessary ?
            
            # Redirect to errors page for this service
            return redirect(reverse('errors')+"?svc_ivoid="+ivoid+"&svc_url="+url)
            

            
class ServicesListViewJson(BaseDatatableView):
    model = Services
    
    columns = [f.name for f in Services._meta.get_fields()] # get all columns from Services in a array
    order_columns = columns # all cols can be ordered
    

        
    # customize the search, when user enter text in the datatable's search box
    def filter_queryset(self, qs):
        logger.info('ServicesListViewJson.filter_queryset') 
        sSearch = self.request.GET.get('search[value]', None) # extract search value from GET string
        #logger.info(sSearch)
        if sSearch:
            logger.info(sSearch)
            qs = qs.filter(Q(ivoid__icontains=sSearch) 
                           | Q(url__icontains=sSearch)
                           | Q(title__icontains=sSearch)
                           | Q(short_name__icontains=sSearch)
                           ) # where to search 
        sRestrict = self.request.GET.get('restrict', None)
        if sRestrict:
            if sRestrict=='result_ok':
                qs = qs.filter(result_vot='yes',result_spec='yes')
            if sRestrict=='result_vot_failed':
                qs = qs.filter(result_vot='no',result_spec='yes')
            if sRestrict=='result_spec_failed':
                qs = qs.filter(result_vot='yes',result_spec='no')
            if sRestrict=='result_all_failed':
                qs = qs.filter(result_vot='no',result_spec='no')
            if sRestrict=='result_no_reply':
                qs = qs.filter(result_vot='',result_spec='')                                            
        return qs
    
    # define initial queryset shown 
    def get_initial_queryset(self):
        logger.info('ServicesListViewJson.get_initial_queryset') 
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        svc_type = self.request.session.get('svc_type',DEFAULT_SVC_TYPE) # get svc_type from session var where we put it or its default value
        svc_date_min = self.request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # get svc_date_min from session var or its default value of today      
    
        qs = Services.objects.filter(svc_type=svc_type,date__gte=svc_date_min)
    
        # check if datatables sent this var
        svc_server = self.request.GET.get('svc_server', None)
                
        if svc_server: # if so, include them in the query
            logger.info('ServicesListViewJson.get_initial_queryset svc_server=%s' % svc_server)   
            qs = qs.filter(url__icontains=svc_server)

        return qs 
    
        #NB can't use .order_by('url').distinct('url') here because order by id is needed for paging
    
    # modify the dict sent back to include stats data needed to draw the pie chart
    def get_context_data(self, *args, **kwargs):
        logger.info('ServicesListViewJson.get_context_data')
        # get dict prepared by BaseDatatableView
        data = super().get_context_data(**kwargs) # get JSON data
        # append data
        #data['test'] = 1000
        # TODO: qs to retrieve stats
        svc_type = self.request.session.get('svc_type',DEFAULT_SVC_TYPE) # get svc_type from session var where we put it or its default value
        svc_date_min = self.request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # get svc_date_min from session var or its default value of today      
        # retrieve queryset with possible filter (from datatables search box)
        qs = self.filter_queryset(self.get_initial_queryset())
        
        # retrieve additionnal statistics - this takes some time        
        nb_result_ok = qs.filter(result_vot='yes',result_spec='yes').count() 
        nb_result_vot_failed = qs.filter(result_vot='no',result_spec='yes').count()
        nb_result_spec_failed = qs.filter(result_vot='yes',result_spec='no').count()
        nb_result_all_failed = qs.filter(result_vot='no',result_spec='no').count()
        nb_result_no_reply = qs.filter(result_vot='',result_spec='').count()
     
        # append statistics to context
        data['nb_result_ok'] = nb_result_ok
        data['nb_result_vot_failed'] = nb_result_vot_failed
        data['nb_result_spec_failed'] = nb_result_spec_failed
        data['nb_result_all_failed'] = nb_result_all_failed
        data['nb_result_no_reply'] = nb_result_no_reply

        #logger.info(data)
        return data
 
 
 
 
    
class ErrorsListView(CustomListView): 
    template_name = 'validation/errors.html'
    form_class = ErrorsListForm
    success_url = 'errors'
    model = Errors
 
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Transmit these GET variables to template
        context['svc_ivoid'] = self.request.GET.get('svc_ivoid',None) 
        context['svc_url'] = self.request.GET.get('svc_url',None)     
        return context

    def form_valid(self, form):
        
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
                 
        type = form.cleaned_data['type'] 
        date_min = form.cleaned_data['date_min']

        logger.info('ErrorsListView.form_valid: form received: new type=%s new date_min=%s' % (type,date_min))

        self.request.session['svc_type'] = type # put svc_type in session var
        self.request.session['svc_date_min'] = str(date_min) # put svc_date_min in session var

        return super().form_valid(form)
        

   
      
class ErrorsListViewJson(BaseDatatableView):
    model = Errors
    
    columns = [f.name for f in Errors._meta.get_fields()] # get all columns from Errors in a array
    order_columns = columns # all cols can be ordered

    # customize the search, when user enter text in the datatable's search box
    def filter_queryset(self, qs):
        logger.info('ErrorsListViewJson.filter_queryset self.request.GET=%s' % self.request.GET)
        sSearch = self.request.GET.get('search[value]', None) # extract search value from GET string
        #logger.info(sSearch)
        if sSearch:
            logger.info(sSearch)
            qs = qs.filter(Q(name__icontains=sSearch) 
                           | Q(type__icontains=sSearch)
                           | Q(msg__icontains=sSearch)
                           | Q(section__icontains=sSearch)
                           | Q(ivoid__icontains=sSearch)
                           | Q(url__icontains=sSearch)
                           ) # where to search 
                                                
        return qs
    
    # define initial queryset shown 
    def get_initial_queryset(self):
        logger.info('ErrorsListViewJson.get_initial_queryset') 
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        svc_type = self.request.session.get('svc_type',DEFAULT_SVC_TYPE) # get svc_type from session var where we put it or its default value
        svc_date_min = self.request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # get svc_date_min from session var or its default value of today      
        qs = Errors.objects.filter(svc_type=svc_type, date__gte=svc_date_min)
                
        # check if datatables sent these
        svc_ivoid = self.request.GET.get('svc_ivoid', None)
        svc_url = self.request.GET.get('svc_url', None)
        
        if svc_ivoid and svc_url: # if so, include them in the query
            svc_url = html.unescape(svc_url) # transform &amp; to &
            logger.info('svc_ivoid=%s svc_url=%s' % (svc_ivoid,svc_url))   
            qs = qs.filter(ivoid=svc_ivoid, url=svc_url)
            
        return qs

    
    
    
   
    
