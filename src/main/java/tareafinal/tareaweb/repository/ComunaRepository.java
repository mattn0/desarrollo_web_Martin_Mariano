package tareafinal.tareaweb.repository;

import tareafinal.tareaweb.model.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface ComunaRepository extends JpaRepository<Comuna, Integer> {
    Page<Comuna> findAllByOrderByIdDesc(Pageable pageable);
}
