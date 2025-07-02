// reservas.js
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar Select2
    $('select').select2({
        theme: 'default',
        width: '100%',
        placeholder: 'Seleccione una opción',
        minimumResultsForSearch: 10
    });

    // Elementos del formulario
    const form = document.getElementById('reservaForm');
    const fechaInput = document.getElementById('id_fecha');
    const horaInput = document.getElementById('id_hora');
    const now = new Date();

    // Configuración inicial
    fechaInput.min = now.toISOString().split('T')[0];
    ajustarHoraMinima();

    // Event Listeners
    fechaInput.addEventListener('change', ajustarHoraMinima);
    horaInput.addEventListener('change', validarIntervalo);

    // Funciones principales
    function ajustarHoraMinima() {
        const fechaSeleccionada = new Date(fechaInput.value);
        const esHoy = fechaSeleccionada.toDateString() === now.toDateString();
        
        if (esHoy) {
            const horaActual = now.getHours();
            const minutosActuales = now.getMinutes();
            
            let horaMinima = horaActual;
            let minutoMinimo = minutosActuales < 30 ? 30 : 0;
            
            if (minutosActuales >= 30) {
                horaMinima += 1;
            }
            
            // Asegurar que esté dentro del rango 11:00 - 23:30
            if (horaMinima < 11) {
                horaMinima = 11;
                minutoMinimo = 0;
            } else if (horaMinima >= 23 && minutoMinimo > 30) {
                horaMinima = 23;
                minutoMinimo = 30;
            }
            
            horaInput.min = `${String(horaMinima).padStart(2, '0')}:${String(minutoMinimo).padStart(2, '0')}`;
        } else {
            horaInput.min = '11:00';
        }
        
        // Validar hora actual si es necesario
        if (horaInput.value && horaInput.value < horaInput.min) {
            horaInput.value = horaInput.min;
        }
    }

    function validarIntervalo() {
        if (!horaInput.value) return;
        
        const [horas, minutos] = horaInput.value.split(':').map(Number);
        
        // Validar formato de 30 minutos
        if (minutos % 30 !== 0) {
            const nuevoMinuto = minutos < 30 ? 0 : 30;
            const nuevaHora = minutos >= 30 ? horas + 1 : horas;
            
            if (nuevaHora > 23) {
                horaInput.value = '23:30';
            } else {
                horaInput.value = `${String(nuevaHora).padStart(2, '0')}:${String(nuevoMinuto).padStart(2, '0')}`;
            }
        }
        
        // Validar rango horario
        if (horaInput.value < '11:00' || horaInput.value > '23:30') {
            horaInput.setCustomValidity('El horario debe ser entre 11:00 y 23:30');
        } else {
            horaInput.setCustomValidity('');
        }
    }

    // Validación antes de enviar
    form.addEventListener('submit', function(e) {
        if (!validarIntervalo()) {
            e.preventDefault();
            horaInput.focus();
        }
    });
});

// Seleccionar el elemento
const comensalesSelect = document.querySelector('.select-comensales');

// Opcional: Cambiar dinámicamente el máximo según necesidades
function actualizarOpcionesComensales(max) {
    const select = comensalesSelect;
    select.innerHTML = ''; // Limpiar opciones
    
    for (let i = 1; i <= max; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        select.appendChild(option);
    }
}
