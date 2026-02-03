"""
Módulo base_dialog.py
Clase base para todos los diálogos de la calculadora.
Proporciona funcionalidad común como cierre con Escape, validación y accesibilidad.
"""

import wx


class DialogoBase(wx.Dialog):
    """
    Clase base para todos los diálogos de la calculadora.
    
    Funcionalidad incluida:
    - Cierre con tecla Escape
    - Validación de números
    - Enfoque de campos con error
    - Layout estandarizado de botones
    - Accesibilidad mejorada
    """
    
    def __init__(self, parent, titulo, tamaño=(450, 400)):
        """
        Inicializa el diálogo base.
        
        Args:
            parent: Ventana padre
            titulo: Título del diálogo
            tamaño: Tupla (ancho, alto) del diálogo
        """
        super().__init__(parent, title=titulo, size=tamaño)
        
        # Vincular tecla Escape para cerrar el diálogo
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key_press)
        
        # Sizer principal que usarán las clases hijas
        self.vbox = wx.BoxSizer(wx.VERTICAL)
    
    def _on_key_press(self, event):
        """Maneja pulsaciones de teclas. Cierra el diálogo con Escape."""
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()
    
    def crear_campo_entrada(self, etiqueta, explicacion=None):
        """
        Crea un campo de entrada con etiqueta y explicación opcional.
        
        Args:
            etiqueta: Texto de la etiqueta
            explicacion: Texto explicativo adicional (opcional)
        
        Returns:
            TextCtrl del campo de entrada
        """
        if explicacion:
            lbl_explicacion = wx.StaticText(self, label=explicacion)
            self.vbox.Add(lbl_explicacion, flag=wx.LEFT | wx.TOP | wx.RIGHT, border=10)
        
        lbl = wx.StaticText(self, label=etiqueta)
        txt = wx.TextCtrl(self)
        self.vbox.Add(lbl, flag=wx.LEFT | wx.TOP, border=10)
        self.vbox.Add(txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        return txt
    
    def crear_campo_resultado(self):
        """
        Crea el campo de resultado de solo lectura.
        
        Returns:
            TextCtrl del campo de resultado
        """
        lbl_resultado = wx.StaticText(self, label="Resultado:")
        txt_resultado = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.vbox.Add(lbl_resultado, flag=wx.LEFT | wx.TOP, border=10)
        self.vbox.Add(txt_resultado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        return txt_resultado
    
    def crear_botones(self, calcular_handler, ayuda_handler):
        """
        Crea los botones estándar: Calcular, Ayuda, Salir.
        
        Args:
            calcular_handler: Función a ejecutar al calcular
            ayuda_handler: Función a ejecutar al mostrar ayuda
        """
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_calcular = wx.Button(self, label="&Calcular")
        btn_calcular.Bind(wx.EVT_BUTTON, calcular_handler)
        
        btn_ayuda = wx.Button(self, label="&Ayuda")
        btn_ayuda.Bind(wx.EVT_BUTTON, ayuda_handler)
        
        btn_salir = wx.Button(self, label="&Salir")
        btn_salir.Bind(wx.EVT_BUTTON, self.salir)
        
        hbox.Add(btn_calcular, flag=wx.RIGHT, border=5)
        hbox.Add(btn_ayuda, flag=wx.RIGHT, border=5)
        hbox.Add(btn_salir)
        
        self.vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)
    
    def finalizar_layout(self):
        """Aplica el sizer al diálogo. Llamar después de añadir todos los elementos."""
        self.SetSizer(self.vbox)
    
    def validar_numero(self, valor_str, control, mensaje_error):
        """
        Valida que una cadena sea un número flotante válido.
        
        Args:
            valor_str: Cadena a validar
            control: Control de entrada asociado (para enfocar en caso de error)
            mensaje_error: Mensaje de error a mostrar si falla
        
        Returns:
            float: El número validado
        
        Raises:
            ValueError: Si la cadena no es un número válido
        """
        try:
            valor = float(valor_str)
            return valor
        except ValueError:
            raise ValueError(mensaje_error)
    
    def validar_entero(self, valor_str, control, mensaje_error):
        """
        Valida que una cadena sea un número entero válido.
        
        Args:
            valor_str: Cadena a validar
            control: Control de entrada asociado
            mensaje_error: Mensaje de error a mostrar si falla
        
        Returns:
            int: El número validado
        
        Raises:
            ValueError: Si la cadena no es un entero válido
        """
        try:
            valor = int(valor_str)
            return valor
        except ValueError:
            raise ValueError(mensaje_error)
    
    def mostrar_error(self, mensaje, titulo="Error de Validación"):
        """
        Muestra un mensaje de error.
        
        Args:
            mensaje: Texto del mensaje de error
            titulo: Título de la ventana de error
        """
        wx.MessageBox(f"Error: {mensaje}", titulo, wx.OK | wx.ICON_ERROR)
    
    def mostrar_info(self, mensaje, titulo="Información"):
        """
        Muestra un mensaje informativo.
        
        Args:
            mensaje: Texto del mensaje
            titulo: Título de la ventana
        """
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)
    
    def salir(self, event=None):
        """Cierra el diálogo actual."""
        self.Destroy()
