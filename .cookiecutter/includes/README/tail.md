## Configuration

| Environment variable     | Usage                                           | Example                                                                                                             |
|--------------------------|-------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `H_BROKER_URL`           | The `h` AMPQ broker                             | `amqp://user:password@rabbit.example.com:5672//`                                                                    |
| `CHECKMATE_BROKER_URL`   | The `checkmate` AMPQ broker                     | `amqp://user:password@rabbit.example.com:5673//`                                                                    |
| `LMS_BROKER_URL`         | The `LMS` AMPQ broker                           | `amqp://user:password@rabbit.example.com:5674//`                                                                    |
| `DISABLE_H_BEAT`         | Whether to disable the `h_beat` process         | `true` to disable the `h_beat` process, `false` to leave it enabled. Defaults to `false` (leave it enabled)         |
| `DISABLE_CHECKMATE_BEAT` | Whether to disable the `checkmate_beat` process | `true` to disable the `checkmate_beat` process, `false` to leave it enabled. Defaults to `false` (leave it enabled) |
| `DISABLE_LMS_BEAT`       | Whether to disable the `lms_beat` process       | `true` to disable, `false` to leave it enabled. Defaults to `false` (leave it enabled)                              |
