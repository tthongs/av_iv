# Mermaid System Architecture Diagrams
## Smart Programmable Power Supply (85–265V AC In, 5–20V / 3A DC Out)

This directory serves as the centralized repository for all **Mermaid architectural flowcharts, block diagrams, and interface charts** for the Smart Programmable Power Supply.

---

### Diagram Catalog

| File Name | Format | Description | Primary Document Reference |
| :--- | :---: | :--- | :--- |
| **[`mcu_system_interaction_and_monitoring.mmd`](mcu_system_interaction_and_monitoring.mmd)** | `.mmd` | **Microcontroller Interconnect & Line-Level Monitoring Diagram**: Shows all lines, buses (I2C, DAC, Sinc3, ADC, SDIO, USB, GPIO), isolation crossings, and peripheral interactions for the STM32G474RET6 MCU. | [Dossier View (`.md`)](mcu_system_interaction_and_monitoring.md) |
| **[`mcu_system_interaction_and_monitoring.md`](mcu_system_interaction_and_monitoring.md)** | `.md` | Full markdown documentation view of the MCU interaction diagram with the signal interface table and circuit derivations. | [SYSTEM_BLOCK_DIAGRAM_AND_ARCHITECTURE.md](../SYSTEM_BLOCK_DIAGRAM_AND_ARCHITECTURE.md) |
| **[`four_stage_power_flow.mmd`](four_stage_power_flow.mmd)** | `.mmd` | **Simplified 4-Stage Power Flow Block Diagram**: High-level power path from Universal AC Mains through Rectifier, Isolated QR Flyback, and Buck-Boost post-regulator to DUT. | [README.md](../../README.md) |
| **[`master_hardware_architecture.mmd`](master_hardware_architecture.mmd)** | `.mmd` | **Master Hardware Architecture Diagram**: Multi-domain hardware flow across Hot Domain, Reinforced Isolation Barrier, SELV Buck-Boost, Control, and Telemetry. | [SYSTEM_BLOCK_DIAGRAM_AND_ARCHITECTURE.md](../SYSTEM_BLOCK_DIAGRAM_AND_ARCHITECTURE.md) |
| **[`component_connections_block_diagram.mmd`](component_connections_block_diagram.mmd)** | `.mmd` | **Detailed Component Connections Block Diagram**: Full pin-to-pin and net-level hardware interconnect diagram connecting all 51 components across AC Mains, 65kHz Flyback, LM5176 Buck-Boost, Telemetry, and MCU. | [PRODUCT_REQUIREMENT_DOCUMENT_PRD.md](../PRODUCT_REQUIREMENT_DOCUMENT_PRD.md) |

---

### How to Render / View

1. **GitHub / GitLab / Markdown Editors**:
   - Open any `.md` file in this directory to see the diagram natively rendered by the integrated Mermaid viewer.
2. **VS Code / Cursor / JetBrains IDE**:
   - Install the **Mermaid Preview** or **Markdown Preview Mermaid Support** extension to view `.mmd` and `.md` files interactively.
3. **Mermaid Live Editor**:
   - Copy and paste the contents of any `.mmd` file into [mermaid.live](https://mermaid.live) to render, customize, or export as SVG/PNG.
