from django.shortcuts import render
import altair as alt
from django.shortcuts import render
from .models import BBRIRecord
import pandas as pd

# Create your views here.
def candlestick_chart_view(request):
    # Query the data from the database
    records = BBRIRecord.objects.all()
    
    # Convert the queryset to a DataFrame
    data = pd.DataFrame.from_records(records.values())

    # Convert the datetime field to pandas datetime
    data['datetime'] = pd.to_datetime(data['datetime'])

    # Create the base chart
    base = alt.Chart(data).encode(
        x=alt.X('datetime:T', title='Date and Time', 
                scale=alt.Scale(domain=(data['datetime'].min(), data['datetime'].max())))
    ).interactive()

    # Create the candlestick bars
    candlestick = base.mark_bar().encode(
        y=alt.Y('open_price:Q', title='Price (IDR)',
                scale=alt.Scale(domain=(data['low_price'].min(), data['high_price'].max()))),
        y2='close_price:Q',
        color=alt.condition("datum.open_price <= datum.close_price",
                            alt.value("#06982d"),  # Green for up days
                            alt.value("#ae1325"))  # Red for down days
    ).properties(
        title='BBRI Hourly Candlestick Chart',
        width=800,  # Set the width to fit the window
        height=400  # Set the height to fit the window
    )

    # Add high-low rules
    high_low = base.mark_rule().encode(
        y='low_price:Q',
        y2='high_price:Q',
        color=alt.condition("datum.open_price <= datum.close_price",
                            alt.value("#06982d"),  # Green for up days
                            alt.value("#ae1325"))  # Red for down days
    )

    # Combine the candlestick bars and high-low rules
    chart = candlestick + high_low

    # Convert the chart to JSON and pass it to the template
    chart_json = chart.to_json()

    return render(request, 'candlestick_chart.html', {'chart_json': chart_json})
