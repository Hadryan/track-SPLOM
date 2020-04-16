async function plot() {

     /* grab data from /data enpoint in flask app */
    var data = await d3.json('/data');
    var features = ['danceability',
                    'energy',
                    'instrumentalness',
                    'speechiness',
                    'tempo',
                    'valence']

    /* define plot dimensions and padding */
    var width = 900,
        height = 900;
        x_range_pad = 40,
        y_range_pad = 90;

    /* create svg element in DOM */
    var svg = d3.select('body').append('div')
        .attr('class', 'container')
        .append('svg')
            .attr('width', width)
            .attr('height', height)
            .style('font', '10px sans-serif');
    
    var feature_scale = d3.scaleBand()
        .domain(features)
        .range([y_range_pad, height - x_range_pad])
        .paddingInner(0.2);
    
    var plot_height = feature_scale.bandwidth();

    var x_scales = {},
        y_scales = {};
    features.forEach(function(feat, i) {
        var extent = d3.extent(data, d => d[feat]);
        x_scales[feat] = d3.scaleLinear()
            .domain(extent)
            .range([0, plot_height])
            .nice();
        y_scales[feat] = d3.scaleLinear()
            .domain(extent)
            .range([plot_height, 0])
            .nice();
    });

    svg.selectAll('columns').data(features).enter().append('g')
        .attr('transform', d => 'translate(' + feature_scale(d) + ',0)')
        .attr('class', 'column')
        .selectAll('rows').data(function(d, i) {
            var unique_rows = features.filter((_, j) => i <= j);
            return unique_rows.map(d_new => [d, d_new]);
        })
        .enter().append('g')
            .attr('transform', d => 'translate(0,' + feature_scale(d[1]) + ')')
            .attr('class', 'splom')
            .selectAll('points').data(function(feat) {
                return data.map(d => [d[feat[0]], d[feat[1]]]);
            })
            .enter().append('circle')
                .attr('r', 1.5)
                .attr('fill', '#3288bd')
                .attr('opacity', 0.75)
    svg.selectAll('.splom').each(function(feat)  {
        var scale_x = x_scales[feat[0]], scale_y = y_scales[feat[1]];
        d3.select(this).selectAll('circle').attr('cx', d => scale_x(d[0])).attr('cy', d => scale_y(d[1]))
        d3.select(this).append('g').attr('transform', 'translate(0,0)').call(d3.axisLeft(scale_y).ticks(4))
        d3.select(this).append('g').attr('transform', 'translate(0,'+plot_height+')').call(d3.axisBottom(scale_x).ticks(4))
    })
    
    svg.append('g')
        .attr('id', 'leftaxis')
        .attr('transform', 'translate(66, 0)')
        .call(d3.axisLeft(feature_scale));
    d3.select('#leftaxis').selectAll('path').remove();
    d3.select('#leftaxis').selectAll('line').remove();

    svg.append('g')
        .attr('id', 'bottomaxis')
        .attr('transform', 'translate(0,' + (height - x_range_pad + 20) + ')')
        .call(d3.axisBottom(feature_scale));
    d3.select('#bottomaxis').selectAll('path').remove();
    d3.select('#bottomaxis').selectAll('line').remove();



    }
plot();