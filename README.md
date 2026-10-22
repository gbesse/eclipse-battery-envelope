# eclipse-battery-envelope

## Français

Propager les bornes de charge sous éclipses et incertitudes.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m eclipse_battery_envelope examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Arithmétique d’intervalles sur production et consommation par segment : réserve, saturation et énergie non servie restent séparées. Le premier franchissement possible de réserve est localisé dans le segment. Contrairement au planificateur de mission, l’outil audite une enveloppe fournie sans choisir des tâches.

### Limites

Modèle énergétique affine explicite, heures/W/Wh, incertitudes rectangulaires indépendantes ; sans température, vieillissement, tension ni validation matérielle. Le pire cas n’est pas une probabilité de panne.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Propagate battery-charge bounds through eclipses and uncertainty.

Synthetic data; no network access or secret required.

```sh
python -m eclipse_battery_envelope examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Interval propagation over piecewise generation and load: reserve, saturation and unserved energy remain separate. The first possible reserve crossing is localized inside a segment. Unlike the mission planner, this audits a supplied envelope without selecting tasks.

### Limits

Explicit affine energy model, hours/W/Wh, independent rectangular uncertainty; no temperature, ageing, voltage or hardware validation. Worst case is not a failure probability.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Propagar cotas de carga durante eclipses e incertidumbre.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m eclipse_battery_envelope examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Propagación de intervalos de generación y consumo por segmento: reserva, saturación y energía no servida quedan separadas. Localiza el primer cruce posible de reserva dentro del segmento. A diferencia del planificador, audita una envolvente dada sin seleccionar tareas.

### Límites

Modelo energético afín explícito, horas/W/Wh e incertidumbre rectangular independiente; sin temperatura, envejecimiento, tensión ni validación física. El peor caso no es probabilidad de fallo.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://github.com/AVSLab/basilisk
- https://github.com/gbesse/mission-intent-repair

## Exemple d’entrée / Input example / Ejemplo de entrada

```json
{
  "capacity_wh": 100,
  "initial_wh": [
    70,
    80
  ],
  "reserve_wh": 20,
  "segments": [
    {
      "id": "sun",
      "duration_hours": 1,
      "generation_w": [
        30,
        40
      ],
      "load_w": [
        10,
        15
      ]
    },
    {
      "id": "eclipse",
      "duration_hours": 2,
      "generation_w": [
        0,
        0
      ],
      "load_w": [
        25,
        35
      ]
    }
  ]
}
```

FR : champs numériques dans les unités de la section méthode ; clés JSON techniques conservées. EN: numeric fields use the method section units; technical JSON keys are preserved. ES: los campos numéricos usan las unidades del método; se conservan las claves JSON técnicas.
