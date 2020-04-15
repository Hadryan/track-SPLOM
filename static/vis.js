async function plot() {
    const data = await d3.json('/data');
    console.log(data)
}
plot();