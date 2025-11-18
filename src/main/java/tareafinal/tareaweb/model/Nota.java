package tareafinal.tareaweb.model;

import jakarta.persistence.*;

@Entity
@Table(name = "nota", schema = "tarea2")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "aviso_id", nullable = false)
    private Aviso aviso;

    @Column(name = "nota", nullable = false)
    private Integer nota;

    // getters y setters
    public Integer getId() { 
        return id; 
    }

    public Aviso getAviso() { 
        return aviso; 
    }
    public void setAviso(Aviso aviso) { 
        this.aviso = aviso; 
    }

    public Integer getNota() { 
        return nota; 
    }
    public void setNota(Integer nota) { 
        this.nota = nota; 
    }
}
