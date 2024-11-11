let simulation;

function fetchGraphData() {
    fetch('http://127.0.0.1:5000/get_network_data')
      .then(response => response.json())
      .then(data => {
        renderGraph(data.nodes, data.links);
      });
}

// function fetch2DCoordinates(word) {
//   fetch(`http://127.0.0.1:5000/get_2d_coordinates?word=${word}`)
//     .then(response => response.json())
//     .then(data => {
//       render2DGraph(data);
//     });
// }


//  graph D3.js
function renderGraph(nodes, links) {
    const width = window.innerWidth;
    const height = 600;

    // Clear any existing SVG elements
    d3.select('#graph').selectAll('*').remove();

    const svg = d3.select('#graph').append('svg')
      .attr('width', width)
      .attr('height', height);

    simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .selectAll('.link')
      .data(links)
      .enter().append('line')
      .attr('class', 'link')
      .attr('stroke-width', d => Math.sqrt(d.value));

    const node = svg.append('g')
      .selectAll('.node')
      .data(nodes)
      .enter().append('g')
      .attr('class', 'node')
      .call(d3.drag()
        .on('start', onDragStart)
        .on('drag', dragged)
        .on('end', onDragEnd));

    node.append('circle')
      .attr('r', 40)  // Adjust the radius to fit the text

    node.append('text')
      .attr('dy', '.25em')
      .attr('text-anchor', 'middle')
      .attr('fill', '#ffffff')  // White text color for contrast
      .text(d => d.id);

    simulation.on('tick', function () {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      node
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });
}

// function render2DGraph(data) {
//   const width = 800;
//   const height = 600;

//   // Clear any existing SVG elements
//   d3.select('#graph').selectAll('*').remove();

//   const svg = d3.select('#graph').append('svg')
//     .attr('width', width)
//     .attr('height', height);

//   const node = svg.selectAll('.node')
//     .data(data)
//     .enter().append('g')
//     .attr('class', 'node')
//     .attr('transform', d => `translate(${d.x},${d.y})`);

//   node.append('circle')
//     .attr('r', 20)  // Adjust the radius to fit the text
//     .attr('fill', '#69b3a2');

//   node.append('text')
//     .attr('dy', '.35em')
//     .attr('text-anchor', 'middle')
//     .attr('fill', '#fff')  // White text color for contrast
//     .text(d => d.word);
// }
function onDragStart(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function onDragEnd(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function addWord() {
    const newWord = document.querySelector('.addWord').value;
    if (newWord) {
      fetch('http://127.0.0.1:5000/add_word', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word: newWord })
      })
      .then(response => response.json())
      .then(() => {
        // After adding a word, refresh the graph
        fetchGraphData();
      });
    }
}

document.querySelector('#loadGraph').addEventListener('click', fetchGraphData);
document.querySelector('#addButton').addEventListener('click', addWord);
// document.querySelector('#word-input').addEventListener('change', function() {
//   const word = this.value;
//   fetch2DCoordinates(word);
// });
