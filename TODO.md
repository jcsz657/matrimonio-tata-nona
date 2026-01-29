# ✅ TODO - Tareas Pendientes y Mejoras Futuras

**Proyecto:** Sistema de Gestión de Matrimonio
**Última Actualización:** 2026-01-29

---

## 🎯 Tareas Inmediatas

### Limpieza de Datos:
- [ ] **Eliminar Whisky duplicado** (línea 16 del CSV tiene valor 0)
  - Mantener solo línea 24 con valor $1,000,000
  - Usar la nueva función de eliminar gastos

### Agregar Gastos Reales:
- [ ] Agregar todos los gastos del matrimonio
- [ ] Confirmar valores con proveedores
- [ ] Registrar abonos ya realizados
- [ ] Actualizar fechas límite de pago

### Verificación:
- [ ] Probar todas las funcionalidades
- [ ] Verificar que se creen backups correctamente
- [ ] Exportar a Excel y verificar formato

---

## 📊 Mejoras de Corto Plazo (1-2 semanas)

### Funcionalidades:
- [ ] **Sistema de notificaciones de fechas límite**
  - Alertas 7 días antes de fecha límite
  - Mostrar en Dashboard
  - Destacar visualmente

- [ ] **Búsqueda por texto libre**
  - Buscar por nombre de gasto
  - Buscar por proveedor
  - Buscar en notas

- [ ] **Ordenamiento personalizado**
  - Arrastrar y soltar gastos
  - Guardar orden preferido

- [ ] **Estadísticas avanzadas**
  - Gasto promedio por categoría
  - Gastos más caros vs más baratos
  - Evolución temporal del gasto

### Visual:
- [ ] **Modo responsive móvil**
  - Adaptar cards para pantallas pequeñas
  - Menú hamburguesa
  - Controles touch-friendly

- [ ] **Tema oscuro**
  - Toggle light/dark mode
  - Persistir preferencia

- [ ] **Avatares de proveedores**
  - Iconos o imágenes por proveedor
  - Hace más visual la lista

---

## 🚀 Mejoras de Medio Plazo (1-2 meses)

### Invitados Interactivos:
- [ ] **Página de gestión de invitados mejorada**
  - Agregar invitados desde la app
  - Editar información de invitados
  - Eliminar invitados
  - Sistema de confirmaciones

- [ ] **Envío de invitaciones**
  - Generar links personalizados
  - Confirmar asistencia online
  - Tracking de confirmaciones

- [ ] **Gestión de mesas**
  - Asignar invitados a mesas
  - Visualizar distribución
  - Optimizar acomodo

### Integración con Servicios:
- [ ] **Integración con Tricount**
  - Sincronizar gastos
  - Importar/exportar
  - Balance de deudas

- [ ] **Exportación avanzada**
  - PDF con formato profesional
  - Gráficos incluidos
  - Logo personalizado

- [ ] **Calendario integrado**
  - Ver fechas límite en calendario
  - Recordatorios automáticos
  - Sincronizar con Google Calendar

### Reportes:
- [ ] **Dashboard de proveedores**
  - Vista por proveedor
  - Historial de pagos
  - Documentos adjuntos

- [ ] **Timeline del matrimonio**
  - Línea de tiempo visual
  - Hitos importantes
  - Cuenta regresiva

---

## 💡 Mejoras de Largo Plazo (3-6 meses)

### Arquitectura:
- [ ] **Migración a Base de Datos**
  - Cambiar de CSV a SQLite
  - Mejor performance
  - Relaciones entre tablas

- [ ] **Sistema de Autenticación**
  - Login seguro
  - Múltiples usuarios
  - Roles (Admin, Editor, Viewer)

- [ ] **API REST**
  - Endpoints para CRUD
  - Integración con otras apps
  - Webhooks

### Deploy:
- [ ] **Desplegar en Streamlit Cloud**
  - Acceso desde cualquier lugar
  - URL personalizada
  - SSL automático

- [ ] **App móvil nativa**
  - iOS y Android
  - Notificaciones push
  - Modo offline

### Funcionalidades Avanzadas:
- [ ] **IA para recomendaciones**
  - Sugerir presupuestos basados en datos
  - Detectar gastos fuera de rango
  - Predecir gastos finales

- [ ] **Modo colaborativo**
  - Edición simultánea
  - Comentarios en gastos
  - Chat integrado

- [ ] **Checklist de tareas**
  - Lista de TODOs del matrimonio
  - Asignar responsables
  - Tracking de progreso

---

## 🐛 Bugs Conocidos y Mejoras Técnicas

### Bugs Menores:
- [ ] **number_input siempre muestra 0**
  - Limitación de Streamlit
  - Considerar text_input con validación

- [ ] **Cache TTL puede causar delay**
  - Optimizar cache strategy
  - Considerar cache más inteligente

### Mejoras de Código:
- [ ] **Tests automatizados**
  - Unit tests para funciones
  - Integration tests para flujos
  - CI/CD pipeline

- [ ] **Logging mejorado**
  - Log de todas las operaciones
  - Tracking de errores
  - Analytics de uso

- [ ] **Manejo de errores robusto**
  - Try-catch en operaciones críticas
  - Mensajes de error más informativos
  - Recovery automático

### Performance:
- [ ] **Optimización de carga**
  - Lazy loading de datos
  - Paginación en tablas grandes
  - Caching más agresivo

- [ ] **Optimización de gráficos**
  - Plotly en modo lightweight
  - Gráficos con menos datos para preview
  - Lazy rendering

---

## 📚 Documentación Pendiente

### Para Usuarios:
- [ ] **Manual de usuario completo**
  - Guía paso a paso
  - Screenshots
  - Videos tutoriales

- [ ] **FAQ**
  - Preguntas frecuentes
  - Troubleshooting
  - Tips y trucos

### Para Desarrolladores:
- [ ] **Guía de contribución**
  - Cómo agregar features
  - Estándares de código
  - Process de PR

- [ ] **Documentación de API**
  - Si se implementa API REST
  - Endpoints y ejemplos
  - Postman collection

---

## 🎨 Diseño y UX

### Mejoras Visuales:
- [ ] **Animaciones sutiles**
  - Transiciones suaves
  - Loading spinners elegantes
  - Feedback visual

- [ ] **Tooltips informativos**
  - Ayuda contextual
  - Shortcuts de teclado
  - Tips útiles

- [ ] **Accesibilidad**
  - ARIA labels
  - Navegación por teclado
  - Contraste mejorado

### Flujos de Usuario:
- [ ] **Onboarding**
  - Tour inicial de la app
  - Tips contextuales
  - Setup wizard

- [ ] **Shortcuts de teclado**
  - Ctrl+N: Nuevo gasto
  - Ctrl+E: Editar
  - Ctrl+F: Buscar

---

## 🔐 Seguridad y Privacidad

### Seguridad:
- [ ] **Encriptación de datos sensibles**
  - Encriptar CSV
  - Passwords seguros
  - HTTPS obligatorio

- [ ] **Audit log**
  - Log de todas las operaciones
  - Quién cambió qué y cuándo
  - Posibilidad de rollback

### Privacidad:
- [ ] **Control de datos**
  - Exportar todos los datos
  - Eliminar cuenta completa
  - GDPR compliance

---

## 📱 Integraciones Futuras

### Servicios Externos:
- [ ] **Google Sheets**
  - Sincronización bidireccional
  - Editar desde Sheets

- [ ] **WhatsApp**
  - Notificaciones por WhatsApp
  - Confirmaciones de invitados

- [ ] **Email**
  - Envío de invitaciones
  - Recordatorios automáticos

- [ ] **Cloud Storage**
  - Google Drive
  - Dropbox
  - OneDrive

---

## 🎯 Prioridades

### Alta Prioridad (Hacer pronto):
1. Limpiar duplicados
2. Agregar gastos reales
3. Sistema de alertas de fechas
4. Búsqueda por texto

### Media Prioridad (Hacer después):
1. Modo responsive móvil
2. Gestión de invitados interactiva
3. Exportación PDF
4. Integración con Tricount

### Baja Prioridad (Nice to have):
1. Tema oscuro
2. App móvil nativa
3. IA para recomendaciones
4. Modo colaborativo

---

## 📊 Métricas de Éxito

### KPIs a Medir:
- [ ] Tiempo promedio para agregar gasto
- [ ] Tiempo promedio para editar gasto
- [ ] Número de errores de usuario
- [ ] Satisfacción del usuario (encuesta)
- [ ] Tasa de uso diario/semanal

---

## 🎉 Features "Wow"

### Ideas Creativas:
- [ ] **Cuenta regresiva visual**
  - Días hasta el matrimonio
  - Animación especial

- [ ] **Modo celebración**
  - Cuando se completa un hito
  - Confetti y animaciones

- [ ] **Comparador de presupuestos**
  - Comparar con matrimonios similares
  - Insights de ahorro

- [ ] **Generador de cronograma**
  - Crear timeline automática
  - Basada en la fecha del matrimonio

---

## 📝 Notas

### Criterios para Agregar Features:
1. ¿Agrega valor real al usuario?
2. ¿Es técnicamente factible?
3. ¿Cuánto tiempo tomará?
4. ¿Qué dependencies agrega?
5. ¿Cómo afecta el performance?

### Antes de Implementar:
- [ ] Documentar el plan
- [ ] Crear backup del código
- [ ] Verificar compatibilidad con datos existentes
- [ ] Probar en entorno de desarrollo
- [ ] Actualizar documentación

---

## ✅ Completadas Recientemente (2026-01-29)

- [x] Sistema de cards expandibles
- [x] Filtros inteligentes
- [x] Edición de gastos
- [x] Eliminación con triple confirmación
- [x] Actualización rápida de pagos
- [x] Backups automáticos
- [x] Validación de duplicados
- [x] Alertas de presupuesto
- [x] Vista previa en tiempo real
- [x] Espaciado elegante
- [x] Documentación exhaustiva

---

**Última Revisión:** 2026-01-29
**Próxima Revisión:** Al agregar nuevas funcionalidades
**Mantenido por:** Equipo de Desarrollo
