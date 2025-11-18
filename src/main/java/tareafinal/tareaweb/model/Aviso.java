package tareafinal.tareaweb.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "aviso_adopcion", schema = "tarea2")
public class Aviso {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "fecha_ingreso", nullable = false)
    private LocalDateTime fechaIngreso;

    @ManyToOne
    @JoinColumn(name = "comuna_id", nullable = false)
    private Comuna comuna;

    private String sector;
    private String nombre;
    private String email;
    private String celular;

    @Column(nullable = false)
    private String tipo; // gato | perro

    private Integer cantidad;
    private Integer edad;

    @Column(name = "unidad_medida", nullable = false)
    private String unidadMedida; // a | m

    @Column(name = "fecha_entrega", nullable = false)
    private LocalDateTime fechaEntrega;

    private String descripcion;

    @OneToMany(mappedBy = "aviso", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Nota> notas;

    // getters y setters

    public Integer getId() { 
        return id; 
    }

    //resto de getters/setters

    public List<Nota> getNotas() { 
        return notas; 
    }
    public void setNotas(List<Nota> notas) { 
        this.notas = notas; 
    }

    @Transient
    public Double getPromedioNotas() {
        if (notas == null || notas.isEmpty()) {
            return null; // se mostrará "-"
        }
        return notas.stream().mapToInt(Nota::getNota).average().orElse(Double.NaN);
    }

    public String getSector(){
        return sector;
    }
    public String getNombre(){
        return nombre;
    }
    public String getEmail(){
        return email;
    }
    public String getCelular(){
        return celular;
    }
    public Integer getCantidad(){
        return cantidad;
    }
    public Integer getEdad(){
        return edad;
    }
    public String getDescripcion(){
        return descripcion;
    }
    public LocalDateTime getFechaIngreso() { 
        return fechaIngreso; 
    }
    public Comuna getComuna() { 
        return comuna; 
    }
    public String getTipo() { 
        return tipo; 
    }
    public String getUnidadMedida() { 
        return unidadMedida; 
    }
}