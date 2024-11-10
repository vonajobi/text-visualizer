function fetchGraphData() {
    fetch('http://127.0.0.1:5000/get_network_data')
      .then(response => response.json())
      .then(data => {
        renderGraph(data.nodes, data.links);
      });
  }

  // Function to render the graph using D3.js
  function renderGraph(nodes, links) {
    const width = 800;
    const height = 600;

    const svg = d3.select('#graph').append('svg')
      .attr('width', width)
      .attr('height', height);

    const simulation = d3.forceSimulation(nodes)
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
      .enter().append('circle')
      .attr('class', 'node')
      .attr('r', 10)
      .attr('fill', '#69b3a2')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    node.append('title')
      .text(d => d.id);

    simulation.on('tick', function () {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    });
  }

  // Function to add a new word
  function addWord() {
    const newWord = document.getElementById('newWord').value;
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

  document.querySelector('#loadGraph').addEventListener('click', fetchGraphData)
  document.querySelector('#addButton').addEventListener('click', addWord)

