from PyQt5.QtCore import Qt, QObject, QUrl
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from PyQt5.QtWebEngine import QWebEngineRegisterProtocolHandlerRequest, QWebEngineClientCertificateSelection
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView, QWebEnginePage, QWebEngineCertificateError
from PyQt5.QtNetwork import QAuthenticator


class WebPage(QWebEnginePage):
    """
    A :class:`QWebEnginePage` that positions common web page notifications correctly for :module:`orchid`.
    """

    def __init__(self, profile: QWebEngineProfile, parent: QObject = None) -> None:
        """
        Creates a :class:`WebPage` with the given web profile and makes connections to handle common signals.

        :param profile: The :class:`QWebEngineProfile` that manages the way this page reacts.
        :type profile: QWebEngineProfile
        :param parent: An optional :class:`QObject` parent for this page.
        :type parent: QObject
        """
        super().__init__(profile, parent)
        self.authenticationRequired.connect(self._on_authentication_required)
        self.featurePermissionRequested.connect(self._on_feature_permission_requested)
        self.proxyAuthenticationRequired.connect(self._on_proxy_authentication_required)
        self.registerProtocolHandlerRequested.connect(self._on_register_protocol_handler_requested)
        self.selectClientCertificate.connect(self._on_select_client_certificate)

    def certificateError(self, error: QWebEngineCertificateError) -> bool:
        """
        Displays a certificate error for the user.

        :return: True if the error was able to be overridden, false otherwise.
        :rtype: bool
        """
        if error.isOverridable():
            dialog = QDialog(self)
            dialog.setModal(True)
            dialog.setWindowFlags(dialog.windowFlags() & Qt.WindowContextHelpButtonHint)
            dialog.setWindowTitle(self.tr("Certificate Error"))
            return dialog.exec() == QDialog.Accepted

        QMessageBox.critical(self, self.tr("Certificate Error"), error.errorDescription())
        return False

    def _on_authentication_required(self, request: QUrl, auth: QAuthenticator) -> None:
        """
        Displays a log in box for the user to attempt to log into the site.

        :param request: The QUrl of the site that requested the log in.
        :type request: QUrl
        :param auth: The :class:`QAuthenticator` that will hold login details for the user.
        :type auth: QAuthenticator
        """
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog.setWindowFlags(dialog.windowFlags() & Qt.WindowContextHelpButtonHint)

        # TODO: Get username and password here.
        # Get the username and password to authenticate.
        # if dialog.exec() == QDialog.Accepted:
        #     auth.setUser()
        #     auth.setPassword()
        # else:
        auth = None

    def _on_feature_permission_requested(self, request: QUrl, feature, Feature) -> None:
        """
        Displays a notification for the user to accept or deny a feature request from a website.

        :param request: The :class:`QUrl` that made the request for the feature.
        :type request: QUrl
        :param feature: The feature that was requested.
        :type feature: Feature
        """
        # Map features to questions to ask the user.
        features = {
            QWebEnginePage.Geolocation: self.tr("Allow {} to access your location information?".format(request.host())),
            QWebEnginePage.MediaAudioCapture: self.tr("Allow {} to access your microphone?".format(request.host())),
            QWebEnginePage.MediaVideoCapture: self.tr("Allow {} to access your webcam?".format(request.host())),
            QWebEnginePage.MediaAudioVideoCapture: self.tr("Allow {} to access your microphone and webcam?".format(request.host())),
            QWebEnginePage.MouseLock: self.tr("Allow {} to lock your mouse cursor?".format(request.host())),
            QWebEnginePage.DesktopVideoCapture: self.tr("Allow {} to capture video of your desktop?".format(request.host())),
            QWebEnginePage.DesktopAudioVideoCapture: self.tr("Allow {} to capture audio and video of your desktop?".format(request.host()))
        }

        # Ask the user if permission should be granted.
        question = features.get(feature, "")
        if not question.isEmpty() and QMessageBox.question(self, self.tr("Permission Request"), question) == QMessageBox.Yes:
            self.setFeaturePermission(request, feature, self.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(request, feature, self.PermissionDeniedByUser)

    def _on_proxy_authentication_required(self, request: QUrl, auth: QAuthenticator, proxy_host: str) -> None:
        """
        Displays a notification for the user to log in to the proxy.

        :param request: The :class:`QUrl` that made the request for the proxy log in.
        :type request: QUrl
        :param auth: The :class:`QAuthenticator` that takes the username and password.
        :type auth: QAuthenticator
        :param proxy_host: The name of the host that made the request for the proxy log in.
        :type proxy_host: str
        """
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog.setWindowFlags(dialog.windowFlags() & Qt.WindowContextHelpButtonHint)

        # TODO: Get username and password here.
        # Get the username and password for the proxy.
        # if dialog.exec() == QDialog.Accepted:
        #     auth.setUser()
        #     auth.setPassword()
        # else:
        auth = None

    def _on_register_protocol_handler_requested(self, request: QWebEngineRegisterProtocolHandlerRequest) -> None:
        """
        Displays a notification for the user to confirm opening specific types of links with a specific handler.

        :param request: The :class:`QWebEngineRegisterProtocolHandlerRequest` that is asking if the handler should be
        allowed to open specific types of links. The type of handler and the type of link are contained in this object.
        :type request: QWebEngineRegisterProtocolHandlerRequest
        """
        answer = QMessageBox.question(self, self.tr("Permission Request"),
                                      self.tr("Allow {} to open all {} links?".format(request.origin().host(),
                                                                                      request.scheme())))
        if answer == QMessageBox.Yes:
            request.accept()
        else:
            request.reject()

    def _on_select_client_certificate(self, selection: QWebEngineClientCertificateSelection) -> None:
        """
        Selects the first client certificates in the given selection.

        :param selection: The :class:`QWebEngineClientCertificateSelection`
        :type selection: QWebEngineClientCertificateSelection
        """
        selection.select(selection.certificates().at(0))  # Select the first certificate.


class WebView(QWebEngineView):
    """"""

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the :class:`WebView` with...
        :param parent: An optional :class:`QWidget` parent for this view.
        """
        super().__init__(parent)

    def set_page(self, page: WebPage) -> None:
        """"""
        action = page.action(WebPage.Forward)
        action.changed.connect()
