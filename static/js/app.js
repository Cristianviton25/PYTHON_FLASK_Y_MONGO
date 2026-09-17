function abrirModalEliminar(idZapato) {
    Swal.fire({
        title: 'Eliminar Zapato',
        text: "¿Está seguro de eliminar este registro?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'NO',
        confirmButtonText: 'SI'
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = "/eliminar/" + idZapato;
        }
    });
}