var vents = {
    items: {
        cliente: '',
        fecha_creacion:'',
        monto:'',
        productos:[]
    },
    add: function(){
    }
};
$(function (){
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear:true,
    });

});