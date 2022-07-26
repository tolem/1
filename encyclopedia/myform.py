from django import forms
# Class which defines new entry form content
class NewWikiForm(forms.Form):
    entry_title = forms.CharField(label="Wiki title",
        min_length=1,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': "Topic title"}) #replaces default widget
        )
    entry_description = forms.CharField(
        label="Description (you can apply Markdown)",
        min_length=1,
        max_length=10000,
        widget=forms.Textarea(attrs={'placeholder': " Add Content?", 'style': 'width:40vw;, height:20vw;'})) #replaces default widget





# Class for editing form content
class EditWikiForm(forms.Form):
    entry_description = forms.CharField(label="\"Description (you can apply Markdown)\"", 
        min_length=1, max_length=10000,widget=forms.Textarea( attrs={'placeholder': " Add Content?", 'style': 'width:40vw;, height:20vw;'}))
