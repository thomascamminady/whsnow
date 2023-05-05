# import altair as alt
# import folium
# import streamlit as st

# from wahoosnowmaker import logger


# @st.cache_data
# def show_chart(df, *args, **kwargs):
#     logger.info("Creating chart.")
#     logger.info(df.columns)

#     base = (
#         alt.Chart(df)
#         .mark_line(clip=True, point=False)
#         .encode(
#             x=alt.X("Elapsed time (seconds):Q", scale=alt.Scale(zero=False)),
#             # y=alt.Y("value:Q", scale=alt.Scale(zero=False)),
#             color=alt.Color("file:N", scale=alt.Scale(scheme="tableau10")),
#             # shape=alt.Shape(":N"),
#             # opacity=alt.condition(legend_selection, alt.value(1), alt.value(0.01)),
#         )
#         .properties(width=1200, height=300)
#         .interactive()
#     )
#     charts = [
#         base.encode(y=alt.Y(variable, scale=alt.Scale(zero=False)))
#         for variable in df.columns
#     ]
#     chart = (
#         alt.vconcat(*charts)
#         .configure_legend(labelLimit=0)
#         .resolve_scale(y="independent")
#     )
#     st.altair_chart(chart, use_container_width=True)


# # @st.cache_data
# def create_map(df):
#     logger.info("Creating map.")
#     meanlat = df["latitude"].mean()
#     meanlon = df["longitude"].mean()
#     map = folium.Map(location=[meanlat, meanlon], zoom_start=10)
#     colors = [
#         "#4c78a8",
#         "#f58518",
#         "#e45756",
#         "#72b7b2",
#         "#54a24b",
#         "#eeca3b",
#         "#b279a2",
#         "#ff9da6",
#         "#9d755d",
#         "#bab0ac",
#     ]
#     for i, (_, groupdf) in enumerate(df.groupby("file")):
#         points = [
#             (lat, lon)
#             for lat, lon in zip(
#                 groupdf["latitude"].to_numpy(),
#                 groupdf["longitude"].to_numpy(),
#                 strict=True,
#             )
#         ]
#         try:
#             folium.PolyLine(
#                 points, color=colors[i % len(colors)], weight=2.5, opacity=1
#             ).add_to(map)
#         except Exception as e:
#             logger.info(e)
#     return map
