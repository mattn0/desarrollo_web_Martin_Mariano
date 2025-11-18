package tareafinal.tareaweb.model;

import jakarta.persistence.*;

@Entity
@Table(name = "comuna", schema = "tarea2")
public class Comuna {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String nombre;

    @Column(name = "region_id", nullable = false)
    private Integer regionId;  // id

    // getters y setters
    public Integer getId() { 
        return id; 
    }
    public void setId(Integer id) { 
        this.id = id; 
    }

    public String getNombre() { 
        return nombre; 
    }
    public void setNombre(String nombre) { 
        this.nombre = nombre; 
    }

    public Integer getRegionId() { 
        return regionId; 
    }
    public void setRegionId(Integer regionId) { 
        this.regionId = regionId; 
    }
}