import plotly.express as px

free_styles = [
    "open-street-map",
    "carto-positron",
    "carto-darkmatter",
    "stamen-terrain",
    "stamen-toner",
    "stamen-watercolor",
]
mapbox_styles = [
    "basic",
    "streets",
    "outdoors",
    "light",
    "dark",
    "satellite",
    "satellite-streets",
]

map_styles = free_styles + mapbox_styles


colorscales = px.colors.named_colorscales()
