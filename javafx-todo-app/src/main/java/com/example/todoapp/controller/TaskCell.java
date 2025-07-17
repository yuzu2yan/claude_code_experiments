package com.example.todoapp.controller;

import com.example.todoapp.model.Task;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.paint.Color;

public class TaskCell extends ListCell<Task> {
    private HBox hbox;
    private CheckBox checkBox;
    private Label label;
    private Button editButton;
    private Button deleteButton;
    
    public TaskCell() {
        super();
        
        checkBox = new CheckBox();
        label = new Label();
        editButton = new Button("Edit");
        deleteButton = new Button("Delete");
        
        editButton.setStyle("-fx-font-size: 10px; -fx-padding: 2 5 2 5;");
        deleteButton.setStyle("-fx-font-size: 10px; -fx-padding: 2 5 2 5;");
        
        HBox.setHgrow(label, Priority.ALWAYS);
        label.setMaxWidth(Double.MAX_VALUE);
        
        hbox = new HBox(10);
        hbox.getChildren().addAll(checkBox, label, editButton, deleteButton);
    }
    
    @Override
    protected void updateItem(Task task, boolean empty) {
        super.updateItem(task, empty);
        
        if (empty || task == null) {
            setGraphic(null);
        } else {
            checkBox.setSelected(task.isCompleted());
            label.setText(task.getDescription());
            
            if (task.isCompleted()) {
                label.setTextFill(Color.GRAY);
                label.setStyle("-fx-strikethrough: true;");
            } else {
                label.setTextFill(Color.BLACK);
                label.setStyle("-fx-strikethrough: false;");
            }
            
            checkBox.setOnAction(e -> {
                task.setCompleted(checkBox.isSelected());
                updateItem(task, false);
            });
            
            editButton.setOnAction(e -> {
                TextInputDialog dialog = new TextInputDialog(task.getDescription());
                dialog.setTitle("Edit Task");
                dialog.setHeaderText("Edit task description:");
                dialog.setContentText("Task:");
                
                dialog.showAndWait().ifPresent(newDescription -> {
                    if (!newDescription.trim().isEmpty()) {
                        task.setDescription(newDescription);
                        updateItem(task, false);
                    }
                });
            });
            
            deleteButton.setOnAction(e -> {
                getListView().getItems().remove(task);
            });
            
            setGraphic(hbox);
        }
    }
}