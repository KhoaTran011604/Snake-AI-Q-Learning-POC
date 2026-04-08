/**
 * Training progress chart using Chart.js.
 * Shows avg score (rolling 50) over episodes.
 */
const TrainingChart = (() => {
  const ctx = document.getElementById("training-chart").getContext("2d");
  let chart = null;
  let bestAvg = 0;

  function init() {
    chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: [],
        datasets: [{
          label: "Avg Score (50 ep)",
          data: [],
          borderColor: "#e94560",
          backgroundColor: "rgba(233, 69, 96, 0.1)",
          fill: true,
          tension: 0.3,
          pointRadius: 0,
          borderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        animation: false,
        scales: {
          x: {
            display: true,
            title: { display: true, text: "Episode", color: "#aaa" },
            ticks: { color: "#666", maxTicksLimit: 10 },
            grid: { color: "rgba(15, 52, 96, 0.3)" },
          },
          y: {
            display: true,
            title: { display: true, text: "Avg Score", color: "#aaa" },
            ticks: { color: "#666" },
            grid: { color: "rgba(15, 52, 96, 0.3)" },
            beginAtZero: true,
          },
        },
        plugins: {
          legend: { display: false },
        },
      },
    });
  }

  function addPoint(episode, avgScore) {
    if (!chart) return;
    chart.data.labels.push(episode);
    chart.data.datasets[0].data.push(avgScore);

    // Keep last 1000 points visible
    if (chart.data.labels.length > 1000) {
      chart.data.labels.shift();
      chart.data.datasets[0].data.shift();
    }

    if (avgScore > bestAvg) bestAvg = avgScore;
    chart.update("none");
  }

  function getBestAvg() { return bestAvg; }

  function reset() {
    if (!chart) return;
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    bestAvg = 0;
    chart.update("none");
  }

  return { init, addPoint, getBestAvg, reset };
})();
