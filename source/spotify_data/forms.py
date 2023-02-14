from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from spotify_data.models import Chart, Rank, Region


class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )


class PassResetForm(PasswordResetForm):

    email = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )


class PassSetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )


class PassChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Old password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )


class RankChartForm(forms.Form):

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31",}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    artist = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Drake",
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="God's Plan",
    )

    def __init__(self, *args, **kwargs):
        super(RankChartForm, self).__init__(*args, **kwargs)
        
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68


class RankChart2Form(forms.Form):

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2020-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    artist = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Drake",
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="God's Plan",
    )
    artist_2 = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Billie Eilish",
    )
    title_2 = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="bad guy",
    )

    def __init__(self, *args, **kwargs):
        super(RankChart2Form, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68


class PopularityChartForm(forms.Form):

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    artist = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Drake",
    )
    top_rank = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )

    def __init__(self, *args, **kwargs):
        super(PopularityChartForm, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["top_rank"].choices = Rank.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68


class PopularityChartForm2(forms.Form):

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    artist = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Drake",
    )
    artist_2 = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Kanye West",
    )
    top_rank = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )

    def __init__(self, *args, **kwargs):
        super(PopularityChartForm2, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["top_rank"].choices = Rank.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68
        self.fields["top_rank"].initial = 20


class ArtistMapPopularityForm(forms.Form):

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    chart = forms.ChoiceField(
        required=True, choices=[], 
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    artist = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Drake",
    )

    def __init__(self, *args, **kwargs):
        super(ArtistMapPopularityForm, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )


class SongMapPopularityForm(forms.Form):

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    artist = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="Dua Lipa",
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"}),
        initial="New Rules",
    )

    def __init__(self, *args, **kwargs):
        super(SongMapPopularityForm, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )


class TopStreamedArtistsForm(forms.Form):

    top_choices = (
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (100, 100),
    )

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    top_streamed = forms.ChoiceField(
        required=True,
        choices=top_choices,
        widget=forms.Select(attrs={"class": "form_widgets"}),
    )

    def __init__(self, *args, **kwargs):
        super(TopStreamedArtistsForm, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68
        self.fields["top_streamed"].initial = 20


class TopStreamedArtistsForm2(forms.Form):

    top_choices = ((5, 5), (10, 10), (15, 15),
                   (20, 20), (30, 30), (40, 40), (50, 50))

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    region_2 = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    top_streamed = forms.ChoiceField(
        required=True,
        choices=top_choices,
        widget=forms.Select(attrs={"class": "form_widgets"}),
    )

    def __init__(self, *args, **kwargs):
        super(TopStreamedArtistsForm2, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68
        self.fields["region_2"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region_2"].initial = 67
        self.fields["top_streamed"].initial = 10


class TopStreamedSongsForm(forms.Form):

    top_choices = (
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (100, 100),
    )

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    top_streamed = forms.ChoiceField(
        required=True,
        choices=top_choices,
        widget=forms.Select(attrs={"class": "form_widgets"}),
    )

    def __init__(self, *args, **kwargs):
        super(TopStreamedSongsForm, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68
        self.fields["top_streamed"].initial = 20


class TopStreamedSongsForm2(forms.Form):

    top_choices = ((5, 5), (10, 10), (15, 15),
                   (20, 20), (30, 30), (40, 40), (50, 50))

    start = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2018-01-01",
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date",
                                      "class": "form_widgets",
                                      "min": "2017-01-01",
                                      "max": "2021-12-31"}),
        initial="2019-01-01",
    )
    region = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    region_2 = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    chart = forms.ChoiceField(
        required=True, choices=[],
        widget=forms.Select(attrs={"class": "form_widgets"})
    )
    top_streamed = forms.ChoiceField(
        required=True,
        choices=top_choices,
        widget=forms.Select(attrs={"class": "form_widgets"}),
    )

    def __init__(self, *args, **kwargs):
        super(TopStreamedSongsForm2, self).__init__(*args, **kwargs)
        self.fields["chart"].choices = Chart.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region"].initial = 68
        self.fields["region_2"].choices = Region.objects.values("id")\
            .values_list(
            "id", "name"
        )
        self.fields["region_2"].initial = 67
        self.fields["top_streamed"].initial = 10
