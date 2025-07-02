document.addEventListener('DOMContentLoaded', function () {
  const filtroCapacidad = document.getElementById('filtroCapacidad');
  const mesasGrid = document.getElementById('mesasGrid');
  const capacidadSpan = document.getElementById('capacidadTotal');
  const capacidadObjetivo = parseInt(capacidadSpan.dataset.comensales);
  const margenExtra = parseInt(capacidadSpan.dataset.margenExtra || 1);

  function aplicarLogicaEspecial(n) {
    return (n % 2 !== 0) || (n === 10);
  }

  function actualizarCapacidadTotal() {
    let capacidadTotal = 0;
    let hayMesaSuficiente = false;

    mesasGrid.querySelectorAll('.mesa-btn.selected').forEach(mesa => {
      const capacidad = parseInt(mesa.getAttribute('data-capacidad'));
      capacidadTotal += capacidad;
      if (capacidad >= capacidadObjetivo) {
        hayMesaSuficiente = true;
      }
    });

    capacidadSpan.textContent = capacidadTotal;

    mesasGrid.querySelectorAll('.mesa-btn').forEach(mesa => {
      const capacidadMesa = parseInt(mesa.getAttribute('data-capacidad'));
      const checkbox = mesa.querySelector('input[type="checkbox"]');
      const estaSeleccionada = mesa.classList.contains('selected');

      if (!estaSeleccionada) {
        // Caso especial: si la reserva es 10, no bloquear la mesa de 12
        if (capacidadObjetivo === 10 && capacidadMesa === 12) {
          mesa.classList.remove('unavailable');
          checkbox.disabled = false;
          return; // no bloquearla
        }

        // Si ya cubrimos los comensales, bloquear las demás mesas
        if (capacidadTotal >= capacidadObjetivo) {
          mesa.classList.add('unavailable');
          checkbox.disabled = true;
          return;
        }

        if (aplicarLogicaEspecial(capacidadObjetivo)) {
          if (hayMesaSuficiente) {
            mesa.classList.add('unavailable');
            checkbox.disabled = true;
          } else {
            if ((capacidadTotal + capacidadMesa) > (capacidadObjetivo + margenExtra)) {
              mesa.classList.add('unavailable');
              checkbox.disabled = true;
            } else {
              mesa.classList.remove('unavailable');
              checkbox.disabled = false;
            }
          }
        } else {
          if ((capacidadTotal + capacidadMesa) > (capacidadObjetivo + margenExtra)) {
            mesa.classList.add('unavailable');
            checkbox.disabled = true;
          } else {
            mesa.classList.remove('unavailable');
            checkbox.disabled = false;
          }
        }
      }
    });
  }

  filtroCapacidad.addEventListener('change', function () {
    const capacidadMin = parseInt(this.value);
    mesasGrid.querySelectorAll('.mesa-btn').forEach(mesa => {
      const capacidad = parseInt(mesa.getAttribute('data-capacidad'));
      mesa.style.display = capacidad >= capacidadMin ? 'block' : 'none';
    });
  });

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
