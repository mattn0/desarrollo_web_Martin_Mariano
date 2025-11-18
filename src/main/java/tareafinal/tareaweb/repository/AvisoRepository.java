package tareafinal.tareaweb.repository;

import tareafinal.tareaweb.model.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface AvisoRepository extends JpaRepository<Aviso, Integer> {
        Page<Aviso> findAllByOrderByIdDesc(Pageable pageable);
}
