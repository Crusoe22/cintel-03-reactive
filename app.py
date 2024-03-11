import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas
from shiny import render
import seaborn as sns

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Nolan's Penguin Data", fillable=True)

#Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    
    # Create a dropdown input to choose a column 
    ui.input_selectize("selected_attribute", "Body Measurement in Millimeters", 
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]) 
    
    # Create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Bin Count", 10)
    
    # Create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Bin Count", 1, 100, 50)

    # Create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_lis", "Selected Species of Penguins", 
                            ["Adelie", "Gentoo", "Chinstrap"], selected="", inline=False)

    # Add a horizontal rule to the sidebar
    ui.hr()

    # Add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/Crusoe22/cintel-02-data.git", target="_blank")


# Plot Charts
with ui.layout_columns():
    @render_plotly  
    def plot_plt():  
        return px.histogram(penguins_df,
            x="body_mass_g",
            title="Penguin Mass",
            labels={"body_mass_g": "Body Mass (g)", "count": "Count"})
        
    @render.plot  
    def plot_sns():  
        return sns.histplot(penguins_df, x="species", kde=False)

# Show Data
with ui.layout_columns():

    @render.data_frame
    def penguins_datatable():
        return render.DataTable(penguins_df) 

    @render.data_frame
    def penguins_grid():
        return render.DataGrid(penguins_df)

#Create Scatter plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
        return px.scatter(penguins_df, x="flipper_length_mm", y="bill_length_mm", color="species", 
                          facet_row="species", facet_col="sex", title="Penguin Scatterplot", labels={"flipper_length_mm": "Flipper Length (mm)", "bill_length_mm": "Bill Length (mm)"})


# Pie Chart plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Pie Chart: Body Mass")

    @render_plotly
    def plotly_pie():
        pie_chart = px.pie(penguins_df, values="body_mass_g", names="island", title="Body mass on Islands")
        return pie_chart

    @render_plotly
    def plotly_pie_s():
        pie_chart = px.pie(penguins_df, values="body_mass_g", names="species", title="Body mass from Species")
        return pie_chart
