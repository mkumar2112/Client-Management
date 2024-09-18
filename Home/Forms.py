from django import forms
from .models import ClientInfo

class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientInfo
        fields = [
            'name', 'phoneNo', 'receiveDate', 'productName', 'productimage',
            'reportedIssue', 'clientNotes', 'assignedTechnician', 
            'estimatedAmount', 'deadline', 'status'
        ]
        widgets = {
            'receiveDate': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'estimatedAmount': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ClientNotesForm(forms.ModelForm):
    class Meta:
        model = ClientInfo
        fields = ['clientNotes']  # Only include the clientNotes field
        widgets = {
            'clientNotes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter notes...'}),
        }


