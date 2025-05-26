module com.window {
    requires javafx.controls;
    requires javafx.fxml;

    opens com.window to javafx.fxml;
    exports com.window;
}
