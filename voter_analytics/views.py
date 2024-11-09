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
    model = Voter
    template_name = 'voters/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = VoterFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data

            filters = {}

            if data['party_affiliation']:
                filters['party_affiliation__in'] = data['party_affiliation'].split(',')
            if data['min_date_of_birth']:
                filters['date_of_birth__gte'] = datetime(int(data['min_date_of_birth']), 1, 1)
            if data['max_date_of_birth']:
                filters['date_of_birth__lte'] = datetime(int(data['max_date_of_birth']), 12, 31)
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
    model = Voter
    template_name = 'voters/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_graphs_context_data())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = VoterFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data

            filters = {}

            if data['party_affiliation']:
                filters['party_affiliation__in'] = data['party_affiliation'].split(',')
            if data['min_date_of_birth']:
                filters['date_of_birth__gte'] = datetime(int(data['min_date_of_birth']), 1, 1)
            if data['max_date_of_birth']:
                filters['date_of_birth__lte'] = datetime(int(data['max_date_of_birth']), 12, 31)
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

        # Create the graphs
        birth_years = list(queryset.values_list('date_of_birth__year', flat=True))
        birth_year_hist = go.Figure(data=[go.Histogram(x=birth_years, nbinsx=50, xbins=dict(start=1900, end=2024, size=1))])
        birth_year_hist.update_layout(
            title='Voter Distribution by Year of Birth',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters',
            bargap=0.1
        )
        birth_year_hist_div = plotly.offline.plot(birth_year_hist, output_type='div')

        party_affiliation_counts = queryset.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_affiliation_pie = go.Figure(data=[go.Pie(labels=[aff['party_affiliation'] for aff in party_affiliation_counts],
                                                      values=[aff['count'] for aff in party_affiliation_counts])])
        party_affiliation_pie.update_layout(
            title='Voter Distribution by Party Affiliation',
            legend_title='Party Affiliation'
        )
        party_affiliation_pie_div = plotly.offline.plot(party_affiliation_pie, output_type='div')

        election_participation = queryset.aggregate(
            v20state_count=Count('v20state'),
            v21town_count=Count('v21town'),
            v21primary_count=Count('v21primary'),
            v22general_count=Count('v22general'),
            v23town_count=Count('v23town'),
        )
        election_participation_hist = go.Figure(data=[go.Bar(x=['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'],
                                                            y=[election_participation['v20state_count'],
                                                               election_participation['v21town_count'],
                                                               election_participation['v21primary_count'],
                                                               election_participation['v22general_count'],
                                                               election_participation['v23town_count']],
                                                            text=[f'{value:,.0f}' for value in [election_participation['v20state_count'],
                                                                                                election_participation['v21town_count'],
                                                                                                election_participation['v21primary_count'],
                                                                                                election_participation['v22general_count'],
                                                                                                election_participation['v23town_count']]]
                                                            )]
                                                            )
        election_participation_hist.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
            bargap=0.1
        )
        election_participation_hist_div = plotly.offline.plot(election_participation_hist, output_type='div')

        return {
            'birth_year_hist_div': birth_year_hist_div,
            'party_affiliation_pie_div': party_affiliation_pie_div,
            'election_participation_hist_div': election_participation_hist_div,
            'filter_form': self.filter_form,
        }

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voters/voter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={self.object.street_number}+{self.object.street_name},+{self.object.zip_code}"
        return context