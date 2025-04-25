document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('salesChart').getContext('2d');
    var salesChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4'],
        datasets: [{
          label: 'Doanh số',
          data: [120, 150, 180, 200],
          backgroundColor: 'rgba(60,141,188,0.2)',
          borderColor: 'rgba(60,141,188,1)',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  });