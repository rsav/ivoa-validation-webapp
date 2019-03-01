from django import forms
from crispy_forms.layout import Submit, Layout, Row, Column, HTML
from crispy_forms.helper import FormHelper
from datetime import date

# Possible choices for service type
CHOICES_SVC_TYPE = (
    ('SIA', 'SIA'),
    ('SSA', 'SSA'),
    ('ConeSearch', 'ConeSearch'),
    ('TAP', 'TAP'),
)

# Default for form when first loaded
DEFAULT_SVC_TYPE='SIA'
DEFAULT_SVC_DATE_MIN=date.today().isoformat() # today in format '2019-01-29'


class ServicesListForm(forms.Form):
    
    type = forms.ChoiceField(label='Service Type:', choices=CHOICES_SVC_TYPE)
    date_min = forms.DateField(label='Min Val Date', widget=forms.DateInput(attrs={'type': 'date' })) #use HTML5 input type=date instead of SelectDateWidget(years=[y for y in range(1970,1972)]))
    
    # hidden fields - they must have required=False else form will be invalid when they are not present !
    ivoid = forms.CharField(required=False, widget = forms.HiddenInput())
    url = forms.CharField(required=False, widget = forms.HiddenInput())
    params = forms.CharField(required=False, widget = forms.HiddenInput())
    spec = forms.CharField(required=False, widget = forms.HiddenInput())
    specv = forms.CharField(required=False, widget = forms.HiddenInput())
    
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)        
                 
        # request is avail here thanks to modif of __init__ above - cf https://stackoverflow.com/questions/52275218/how-to-access-session-variable-inside-form-class         
        self.fields['type'].initial=request.session.get('svc_type',DEFAULT_SVC_TYPE) # initial value of the type menu is taken from session var, or default value
        self.fields['date_min'].initial=request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # initial value of the date_min field is taken from session va, or default value       
                 
        self.helper = FormHelper() # defined here, it is an instance variable
 
        self.helper.form_id = 'servicesForm' # give an id to the form so that we can interact with it in the template
        
        #self.helper.form_class = 'form-inline'
        self.helper.layout = Layout( 
            Row(
                Column('type', css_class='form-group'),
                HTML('&nbsp;'), # separator
                Column('date_min',css_class='form-group'),
                HTML('&nbsp;'), # separator
                Column('ivoid'),
                Column('url'), 
                Column('params'), 
                Column('spec'),
                Column('specv'),
                Submit('display', 'Display', title='Redisplay this page using the form parameters', onClick="buttonClicked=1", css_class='form-group'),
                HTML('&nbsp;'), # separator
                Submit('validate', 'Validate', title='Validate the selected service now', onClick="buttonClicked=2", css_class='form-group'),
                HTML('&nbsp;'), # separator
                Submit('errors', 'Errors', title='Display errors for the selected service', onClick="buttonClicked=3", css_class='form-group'),
                css_class='form-inline'
            ),
        )
        
class ServersListForm(forms.Form):
    
    type = forms.ChoiceField(label='Service Type:',choices=CHOICES_SVC_TYPE)
    date_min = forms.DateField(label='Min Val Date',widget=forms.DateInput(attrs={'type': 'date' })) #use HTML5 input type=date instead of SelectDateWidget(years=[y for y in range(1970,1972)]))
    
    # hidden fields - they must have required=False else form will be invalid when they are not present !    
    server = forms.CharField(required=False, widget = forms.HiddenInput())
    
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)        
                 
        # request is avail here thanks to modif of __init__ above - cf https://stackoverflow.com/questions/52275218/how-to-access-session-variable-inside-form-class         
        self.fields['type'].initial=request.session.get('svc_type',DEFAULT_SVC_TYPE) # initial value of the type menu is taken from session var, or default value
        self.fields['date_min'].initial=request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # initial value of the date_min field is taken from session va, or default value       
     
        self.helper = FormHelper() # defined here, it is an instance variable
 
        self.helper.form_id = 'serversForm' # give an id to the form so that we can interact with it in the template
        
 
        #self.helper.form_class = 'form-inline'
        self.helper.layout = Layout( 
            Row(
                Column('type'), #css_class='form-group col-md-2 mb-0'),
                HTML('&nbsp;'), # separator
                Column('date_min'), #css_class='form-group col-md-2 mb-0'),
                Column('server'),
                HTML('&nbsp;'), # separator
                Submit('display', 'Display', title='Redisplay this page using the form parameters', onClick="buttonClicked=1"),
                HTML('&nbsp;'), # separator
                Submit('services', 'Services', title='Display services for the selected server', onClick="buttonClicked=2"),
                HTML('&nbsp;'), # separator
                Submit('efreqs', 'Errors Frequency', title='Display errors frequency for the selected service', onClick="buttonClicked=3", css_class='form-group'),
                css_class='form-inline'
            ),
        )
        
        
class EfreqsListForm(forms.Form):
    
    type = forms.ChoiceField(label='Service Type:',choices=CHOICES_SVC_TYPE)
    date_min = forms.DateField(label='Min Val Date',widget=forms.DateInput(attrs={'type': 'date' })) #use HTML5 input type=date instead of SelectDateWidget(years=[y for y in range(1970,1972)]))
    

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)        
                 
        # request is avail here thanks to modif of __init__ above - cf https://stackoverflow.com/questions/52275218/how-to-access-session-variable-inside-form-class         
        self.fields['type'].initial=request.session.get('svc_type',DEFAULT_SVC_TYPE) # initial value of the type menu is taken from session var, or default value
        self.fields['date_min'].initial=request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # initial value of the date_min field is taken from session va, or default value       
     
        self.helper = FormHelper() # defined here, it is an instance variable
 
        self.helper.form_id = 'efreqsForm' # give an id to the form so that we can interact with it in the template
        
 
        #self.helper.form_class = 'form-inline'
        self.helper.layout = Layout( 
            Row(
                Column('type'), #css_class='form-group col-md-2 mb-0'),
                HTML('&nbsp;'), # separator
                Column('date_min'), #css_class='form-group col-md-2 mb-0'),
                HTML('&nbsp;'), # separator
                Submit('display', 'Display', title='Redisplay this page using the form parameters', onClick="buttonClicked=1"),
                css_class='form-inline',
            ),
        )
        
        

    
class ErrorsListForm(forms.Form):
    
    type = forms.ChoiceField(label='Service Type:',choices=CHOICES_SVC_TYPE)
    date_min = forms.DateField(label='Min Val Date',widget=forms.DateInput(attrs={'type': 'date' })) #use HTML5 input type=date instead of SelectDateWidget(years=[y for y in range(1970,1972)]))
    
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)        
                 
        # request is avail here thanks to modif of __init__ above - cf https://stackoverflow.com/questions/52275218/how-to-access-session-variable-inside-form-class         
        self.fields['type'].initial=request.session.get('svc_type',DEFAULT_SVC_TYPE) # initial value of the type menu is taken from session var, or default value
        self.fields['date_min'].initial=request.session.get('svc_date_min',DEFAULT_SVC_DATE_MIN) # initial value of the date_min field is taken from session va, or default value       
     
        self.helper = FormHelper() # defined here, it is an instance variable
 
        #self.helper.form_class = 'form-inline'
        self.helper.layout = Layout( 
            Row(
                Column('type'), #css_class='form-group col-md-2 mb-0'),
                HTML('&nbsp;'), # separator
                Column('date_min'), #css_class='form-group col-md-2 mb-0'),
                HTML('&nbsp;'), # separator
                Submit('display', 'Display', title='Redisplay this page using the form parameters'),
                css_class='form-inline'
            ),
        )
        
        


              