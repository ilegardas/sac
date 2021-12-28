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
        language: 'es'
    });
    //busqueda de productos
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
    $('input[name="search2"]').autocomplete({
      source: availableTags
    });
});