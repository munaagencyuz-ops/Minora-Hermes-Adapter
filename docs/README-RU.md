# Кратко на русском

`Minora-Hermes-Adapter` — только мост между Hermes и независимым `Minora-Control-Plane`.

Он должен:

- зарегистрировать реальные Hermes tools/hooks;
- связать Hermes session с Minora project;
- отправлять фактические user turns в Control Plane;
- вызвать настоящий `kanban_create`, а не придумать task ID;
- получить реальный task ID и сохранить его;
- запускать правильный Bot/Profile;
- передавать артефакт на validator;
- не решать самостоятельно, какой этап разрешён.

Fixture-тест не называется live E2E. Live E2E обязан пройти через реальный Hermes, Kanban, Bot и новые исходные документы.
