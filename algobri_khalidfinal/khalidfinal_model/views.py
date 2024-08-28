from django.shortcuts import render
import altair as alt
from django.shortcuts import render
from .models import BBRIRecord
import pandas as pd

def candlestick_chart_view(request):
    records = BBRIRecord.objects.all()
    
    data = pd.DataFrame.from_records(records.values())

    data['datetime'] = pd.to_datetime(data['datetime'])

    base = alt.Chart(data).encode(
        x=alt.X('datetime:T', title='Date and Time', 
                scale=alt.Scale(domain=(data['datetime'].min(), data['datetime'].max())))
    ).interactive()

    candlestick = base.mark_bar().encode(
        y=alt.Y('open_price:Q', title='Price (IDR)',
                scale=alt.Scale(domain=(data['low_price'].min(), data['high_price'].max()))),
        y2='close_price:Q',
        color=alt.condition("datum.open_price <= datum.close_price",
                            alt.value("#06982d"),  # Green
                            alt.value("#ae1325"))  # Red
    ).properties(
        title='BBRI Hourly Candlestick Chart',
        width=800,
        height=400 
    )

    high_low = base.mark_rule().encode(
        y='low_price:Q',
        y2='high_price:Q',
        color=alt.condition("datum.open_price <= datum.close_price",
                            alt.value("#06982d"),  # Green
                            alt.value("#ae1325"))  # Red
    )

    chart = candlestick + high_low

    chart_json = chart.to_json()

    return render(request, 'candlestick_chart.html', {'chart_json': chart_json})
