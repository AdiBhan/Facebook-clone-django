from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
import plotly
from .models import Voter
import plotly.graph_objects as go
from django.db.models import Count  # Add this import

# Create your views here.

from .forms import VoterFilterForm

from datetime import datetime


class VoterListView(ListView):
    # Displays list of voters with filtering options for user
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100   # Show 100 results per page
    ordering = ['-date_of_birth']  # Order by date of birth in descending order


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context

    def get_queryset(self):
     # Returns a filtered queryset of voters based on filter form input
        queryset = super().get_queryset()
        self.filter_form = VoterFilterForm(self.request.GET)


        # Applying filters if the form is valid
        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data

            filters = {}
          # Adding filters based on form data
            if data['party_affiliation']:
                filters['party_affiliation__in'] = data['party_affiliation'].split(
                    ',')
            if data['min_date_of_birth']:
                filters['date_of_birth__gte'] = datetime(
                    int(data['min_date_of_birth']), 1, 1)
            if data['max_date_of_birth']:
                filters['date_of_birth__lte'] = datetime(
                    int(data['max_date_of_birth']), 12, 31)
            if data['voter_score']:
                filters['voter_score__in'] = data['voter_score'].split(',')
            filters['v20state'] = data['voted_in_v20state']
            filters['v21town'] = data['voted_in_v21town']
            filters['v21primary'] = data['voted_in_v21primary']
            filters['v22general'] = data['voted_in_v22general']
            filters['v23town'] = data['voted_in_v23town']

            queryset = queryset.filter(**filters)

        return queryset


class VoterGraphsView(ListView):
    # Displays graphs related to voter data
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_graphs_context_data())
        return context

    def get_queryset(self):
        # Returns a filtered queryset of voters based on filter form input, similar to VoterListView
        queryset = super().get_queryset()
        self.filter_form = VoterFilterForm(self.request.GET)


        # Applying filters if the form is valid
        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data
            # print("DATA", data)

            filters = {}
          # Adding filters based on form data
            if data['party_affiliation']:
                filters['party_affiliation__in'] = data['party_affiliation'].split(
                    ',')
            if data['min_date_of_birth']:
                filters['date_of_birth__gte'] = datetime(
                    int(data['min_date_of_birth']), 1, 1)
            if data['max_date_of_birth']:
                filters['date_of_birth__lte'] = datetime(
                    int(data['max_date_of_birth']), 12, 31)
            if data['voter_score']:
                filters['voter_score__in'] = data['voter_score'].split(',')
            filters['v20state'] = data['voted_in_v20state']
            filters['v21town'] = data['voted_in_v21town']
            filters['v21primary'] = data['voted_in_v21primary']
            filters['v22general'] = data['voted_in_v22general']
            filters['v23town'] = data['voted_in_v23town']

            queryset = queryset.filter(**filters)

        return queryset

    def get_graphs_context_data(self):
        queryset = self.get_queryset()
        # Histogram for voter distribution by year of birth
        birth_years = list(queryset.values_list(
            'date_of_birth__year', flat=True))
        print(birth_years)
        birth_year_hist = go.Figure(data=[go.Histogram(
            x=birth_years, nbinsx=50, xbins=dict(start=1900, end=2024, size=1))])
        birth_year_hist.update_layout(
            title='Voter Distribution by Year of Birth',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters',
            bargap=0.1
        )
        
        birth_year_hist_div = plotly.offline.plot(
            birth_year_hist, output_type='div')
        # Pie chart for voter distribution by party affiliation
        party_affiliation_counts = queryset.values(
            'party_affiliation').annotate(count=Count('party_affiliation'))
        party_affiliation_pie = go.Figure(data=[go.Pie(labels=[aff['party_affiliation'] for aff in party_affiliation_counts],
                                                       values=[aff['count'] for aff in party_affiliation_counts])])
        party_affiliation_pie.update_layout(
            title='Voter Distribution by Party Affiliation',
            legend_title='Party Affiliation'
        )
        party_affiliation_pie_div = plotly.offline.plot(
            party_affiliation_pie, output_type='div')

        election_participation = queryset.aggregate(
            v20state_count=Count('v20state'),
            v21town_count=Count('v21town'),
            v21primary_count=Count('v21primary'),
            v22general_count=Count('v22general'),
            v23town_count=Count('v23town'),
        )
        # Bar chart for voter participation by election
        election_participation_hist = go.Figure(data=[go.Bar(x=['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'],
                                                             y=[election_participation['v20state_count'],
                                                                election_participation['v21town_count'],
                                                                election_participation['v21primary_count'],
                                                                election_participation['v22general_count'],
                                                                election_participation['v23town_count']],
                                                             text=[f'{value:,.0f}' for value in [election_participation['v20state_count'],
                                                                                                 election_participation[
                                                                 'v21town_count'],
                                                                 election_participation[
                                                                 'v21primary_count'],
                                                                 election_participation[
                                                                 'v22general_count'],
                                                                 election_participation['v23town_count']]]
                                                             )]
                                                )
        election_participation_hist.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
            bargap=0.1
        )
        election_participation_hist_div = plotly.offline.plot(
            election_participation_hist, output_type='div')
        # Returns graph divs to be used in template
        return {
            'birth_year_hist_div': birth_year_hist_div,
            'party_affiliation_pie_div': party_affiliation_pie_div,
            'election_participation_hist_div': election_participation_hist_div,
            'filter_form': self.filter_form,
        }


class VoterDetailView(DetailView):
    # Displays a single voter's information
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate Google Maps URL based on voter's address
        context['google_maps_url'] = (
            f"https://www.google.com/maps/search/?api=1&query="
            f"{self.object.street_number}+{self.object.street_name},+{self.object.zip_code}"
        )
        return context
