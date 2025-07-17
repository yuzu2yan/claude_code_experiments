package com.example.todoapp;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;

public class TodoApp extends Application {

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Todo List Application");

        // Create the main layout
        BorderPane root = new BorderPane();
        root.setPadding(new Insets(10));

        // Create the header
        Label headerLabel = new Label("My Todo List");
        headerLabel.setStyle("-fx-font-size: 24px; -fx-font-weight: bold;");
        HBox header = new HBox(headerLabel);
        header.setPadding(new Insets(10));
        root.setTop(header);

        // Create the task list view
        ListView<String> taskListView = new ListView<>();
        taskListView.setPrefHeight(300);
        
        // Create input area
        TextField taskInput = new TextField();
        taskInput.setPromptText("Enter a new task...");
        taskInput.setPrefWidth(300);
        
        Button addButton = new Button("Add Task");
        Button deleteButton = new Button("Delete Selected");
        Button clearAllButton = new Button("Clear All");
        
        HBox inputBox = new HBox(10);
        inputBox.getChildren().addAll(taskInput, addButton, deleteButton, clearAllButton);
        inputBox.setPadding(new Insets(10));
        
        // Add event handlers
        addButton.setOnAction(e -> {
            String task = taskInput.getText().trim();
            if (!task.isEmpty()) {
                taskListView.getItems().add(task);
                taskInput.clear();
            }
        });
        
        deleteButton.setOnAction(e -> {
            int selectedIndex = taskListView.getSelectionModel().getSelectedIndex();
            if (selectedIndex >= 0) {
                taskListView.getItems().remove(selectedIndex);
            }
        });
        
        clearAllButton.setOnAction(e -> {
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("Clear All Tasks");
            alert.setHeaderText("Are you sure you want to delete all tasks?");
            alert.setContentText("This action cannot be undone.");
            
            alert.showAndWait().ifPresent(response -> {
                if (response == ButtonType.OK) {
                    taskListView.getItems().clear();
                }
            });
        });
        
        // Allow Enter key to add task
        taskInput.setOnAction(e -> addButton.fire());
        
        // Layout the center content
        VBox centerContent = new VBox(10);
        centerContent.getChildren().addAll(taskListView, inputBox);
        centerContent.setPadding(new Insets(10));
        root.setCenter(centerContent);
        
        // Create status bar
        Label statusLabel = new Label("Ready");
        HBox statusBar = new HBox(statusLabel);
        statusBar.setPadding(new Insets(5));
        statusBar.setStyle("-fx-background-color: #f0f0f0;");
        root.setBottom(statusBar);
        
        // Update status when tasks change
        taskListView.getItems().addListener((javafx.collections.ListChangeListener<String>) c -> {
            int count = taskListView.getItems().size();
            statusLabel.setText(count + " task(s) in list");
        });
        
        // Create and show the scene
        Scene scene = new Scene(root, 600, 500);
        primaryStage.setScene(scene);
        primaryStage.show();
        
        // Focus on input field
        taskInput.requestFocus();
    }

    public static void main(String[] args) {
        launch(args);
    }
}