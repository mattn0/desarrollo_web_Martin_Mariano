package tareafinal.tareaweb.controller;

import tareafinal.tareaweb.model.*;
import tareafinal.tareaweb.repository.*;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Controller
@RequestMapping("/avisos") 
public class AvisoController {
    
    private final AvisoRepository avisoRepo;
    private final NotaRepository notaRepo;

    public AvisoController(AvisoRepository avisoRepo, NotaRepository notaRepo) {
        this.avisoRepo = avisoRepo;
        this.notaRepo = notaRepo;
    }

    // Mostrar tabla con avisos + promedio de notas
    @GetMapping
    public String listarAvisos(Model model) {
        model.addAttribute("avisos", avisoRepo.findAll());
        return "lista_avisos"; // templates
    }

    // asíncrono para agregar nota
    @PostMapping("/{id}/nota")
    @ResponseBody
    public ResponseEntity<?> agregarNota(@PathVariable Integer id, @RequestBody Map<String, Integer> body) {

        // mismo comentario que esta en la validacion de lista_avisos.html
        Integer valor = body.get("nota");
        if (valor == null || valor < 1 || valor > 7) {
            Map<String, String> error = new HashMap<>();
            error.put("mensaje", "La nota debe ser un entero entre 1 y 7");
            return ResponseEntity.badRequest().body(error);
        }

        Optional<Aviso> optAviso = avisoRepo.findById(id);
        if (optAviso.isEmpty()) {
            Map<String, String> error = new HashMap<>();
            error.put("mensaje", "Aviso no encontrado");
            return ResponseEntity.badRequest().body(error);
        }

        Aviso aviso = optAviso.get();
        Nota n = new Nota();
        n.setAviso(aviso);
        n.setNota(valor);
        notaRepo.save(n);

        Double nuevoPromedio = notaRepo.promedioPorAviso(id);

        Map<String, Object> resp = new HashMap<>();
        resp.put("promedio", nuevoPromedio);
        return ResponseEntity.ok(resp);
    }
}
