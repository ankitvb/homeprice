function plot_histogram(hist_data, zip){
    var histPlot = document.getElementById('histogram');

    console.log(hist_data);

    trace_f = {
        x: hist_data['F'],
        opacity: 0.75,
        type: 'histogram',
        name: 'Flat'
        };

    trace_t = {
        x: hist_data['T'],
        opacity: 0.75,
        type: 'histogram',
        name: 'Terrace'
        };

    trace_d = {
        x: hist_data['D'],
        opacity: 0.75,
        type: 'histogram',
        name: 'Detached'
        };

    trace_s = {
        x: hist_data['S'],
        opacity: 0.75,
        type: 'histogram',
        name: 'Semi-Detached'
        };

    data = [trace_f, trace_t, trace_d, trace_s];

    layout = {
        title: 'Range of prices in ' + zip.toUpperCase(),
        xaxis: {title: 'Price in &pound;'},
        yaxis: {title: 'Homes sold'},
        barmode: 'overlay'
    };

    Plotly.plot(histPlot, data, layout)
}


function plot_yearly_mean(mean_year_inout, mean_year_out, vol_year_inout, vol_year_out, zip){
    var yearlyPrice = document.getElementById('meanYearlyPrice');
    var yearlyVol = document.getElementById('meanYearlyVol');

    var inout = zip.toUpperCase();
    var out = inout.split(' ')[0];

    // Plotting yearly mean
    var trace1 = {
           x: [2011, 2012, 2013, 2014, 2015, 2016],
           y: [mean_year_inout[2011], mean_year_inout[2012],
               mean_year_inout[2013], mean_year_inout[2014],
               mean_year_inout[2015], mean_year_inout[2016]],
               name: inout
             };

    var trace2 = {
        x: [2011, 2012, 2013, 2014, 2015, 2016],
        y: [mean_year_out[2011], mean_year_out[2012],
            mean_year_out[2013], mean_year_out[2014],
            mean_year_out[2015], mean_year_out[2016]],
            name: out
          };

    var data_mean = [trace1, trace2]

    var layout_mean = {
        title: 'Mean Price (&pound;)'
        };

    Plotly.plot(yearlyPrice, data_mean, layout_mean, zip);

    // Plotting yearly volume
    var trace3 = {
           x: [2011, 2012, 2013, 2014, 2015, 2016],
           y: [vol_year_inout[2011], vol_year_inout[2012],
               vol_year_inout[2013], vol_year_inout[2014],
               vol_year_inout[2015], vol_year_inout[2016]],
               name: inout
             };

    var trace4 = {
        x: [2011, 2012, 2013, 2014, 2015, 2016],
        y: [vol_year_out[2011], vol_year_out[2012],
            vol_year_out[2013], vol_year_out[2014],
            vol_year_out[2015], vol_year_out[2016]],
            name: out
          };

    var data_vol = [trace3, trace4];

    var layout_vol = {
        title: 'Units Sold'
        };

    Plotly.plot(yearlyVol, data_vol, layout_vol);

    return true;
}



function plot_typewise_mean(mean_type_inout, mean_type_out, zip){
    var typePrice = document.getElementById('meanTypePrice');

    var inout = zip.toUpperCase();
    var out = inout.split(' ')[0];

    var trace1 = {
        x:['Flat','Terrace','Detached','Semi-Detached'],
        y:[mean_type_inout['F'], mean_type_inout['T'],
           mean_type_inout['D'], mean_type_inout['S']],
           name: inout,
           type: 'bar'
    };

    var trace2 = {
        x:['Flat','Terrace','Detached','Semi-Detached'],
        y:[mean_type_out['F'], mean_type_out['T'],
           mean_type_out['D'], mean_type_out['S']],
           name:out,
           type: 'bar'
    };

    var data_type_price = [trace1, trace2]

    var layout_type = {
        title: 'Mean Price by Home Type'
        };

    Plotly.plot(typePrice, data_type_price, layout_type)

}
