Class summary for each class in the project.


**Classes**:

- **Main**: Main class that controls the game.

- **CameraHandler**: Control the FPS-like camera, receiving mouse input.

- **InputHandler**: Manages the user input, directing to the GUI, camera, etc.

- **PlayerHUD**: Manages the 2D layer displaying extra information in the character "vision", such as Health points, bullets left, etc.

- **Player**: Represents the player itself, with a model, collision nodes, shooting bullets, status (health). Later inheriting from creature.

- **Map**: Represents the Map, with a model and properties, such as mist(fog) and etc.

- **Enemy**: Represents the enemy, and similar to Player. Later inheriting from creature.

- **EnemyManager**: Manages the waves of enemies in the stage.