document.addEventListener('DOMContentLoaded', function () {
  const filtroCapacidad = document.getElementById('filtroCapacidad');
  const mesasGrid = document.getElementById('mesasGrid');
  const capacidadSpan = document.getElementById('capacidadTotal');
  const capacidadObjetivo = parseInt(capacidadSpan.dataset.comensales);
  const margenExtra = parseInt(capacidadSpan.dataset.margenExtra || 0);

  function actualizarCapacidadTotal() {
    let capacidadTotal = 0;
    mesasGrid.querySelectorAll('.mesa-btn.selected').forEach(mesa => {
      const capacidad = parseInt(mesa.getAttribute('data-capacidad'));
      capacidadTotal += capacidad;
    });
    capacidadSpan.textContent = capacidadTotal;

    const limite = capacidadObjetivo + margenExtra;

    // Bloquear mesas si se supera el límite
    mesasGrid.querySelectorAll('.mesa-btn').forEach(mesa => {
      const capacidadMesa = parseInt(mesa.getAttribute('data-capacidad'));
      const checkbox = mesa.querySelector('input[type="checkbox"]');

      const estaSeleccionada = mesa.classList.contains('selected');

      if (
        !estaSeleccionada &&
        (capacidadTotal + capacidadMesa) > limite
      ) {
        mesa.classList.add('unavailable');
        checkbox.disabled = true;
      } else if (!checkbox.hasAttribute('data-permanently-disabled')) {
        mesa.classList.remove('unavailable');
        checkbox.disabled = false;
      }
    });
  }

  // Filtrado por capacidad mínima
  filtroCapacidad.addEventListener('change', function () {
    const capacidadMin = parseInt(this.value);
    mesasGrid.querySelectorAll('.mesa-btn').forEach(mesa => {
      const capacidad = parseInt(mesa.getAttribute('data-capacidad'));
      mesa.style.display = capacidad >= capacidadMin ? 'block' : 'none';
    });
  });

  // Selección de mesas visual
  mesasGrid.querySelectorAll('.mesa-btn').forEach(mesa => {
    const checkbox = mesa.querySelector('input[type="checkbox"]');

    if (checkbox.disabled) {
      checkbox.setAttribute('data-permanently-disabled', 'true');
    }

    mesa.addEventListener('click', function () {
      if (checkbox.disabled) return;

      checkbox.checked = !checkbox.checked;
      mesa.classList.toggle('selected', checkbox.checked);

      actualizarCapacidadTotal();
    });
  });

  actualizarCapacidadTotal();
});
