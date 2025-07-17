package com.example.todoapp;

import com.example.todoapp.controller.TaskCell;
import com.example.todoapp.model.Task;
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;

public class EnhancedTodoApp extends Application {
    private ObservableList<Task> tasks = FXCollections.observableArrayList();
    private FilteredList<Task> filteredTasks;
    
    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Enhanced Todo List");
        
        BorderPane root = new BorderPane();
        root.setPadding(new Insets(10));
        
        // Header
        Label headerLabel = new Label("Enhanced Todo List");
        headerLabel.setStyle("-fx-font-size: 28px; -fx-font-weight: bold; -fx-text-fill: #2196F3;");
        
        // Filter buttons
        ToggleGroup filterGroup = new ToggleGroup();
        RadioButton allFilter = new RadioButton("All");
        RadioButton activeFilter = new RadioButton("Active");
        RadioButton completedFilter = new RadioButton("Completed");
        allFilter.setToggleGroup(filterGroup);
        activeFilter.setToggleGroup(filterGroup);
        completedFilter.setToggleGroup(filterGroup);
        allFilter.setSelected(true);
        
        HBox filterBox = new HBox(10);
        filterBox.getChildren().addAll(new Label("Show:"), allFilter, activeFilter, completedFilter);
        
        VBox headerBox = new VBox(10);
        headerBox.getChildren().addAll(headerLabel, filterBox);
        headerBox.setPadding(new Insets(10));
        root.setTop(headerBox);
        
        // Task list
        filteredTasks = new FilteredList<>(tasks, p -> true);
        ListView<Task> taskListView = new ListView<>(filteredTasks);
        taskListView.setCellFactory(param -> new TaskCell());
        taskListView.setPrefHeight(400);
        
        // Input area
        TextField taskInput = new TextField();
        taskInput.setPromptText("What needs to be done?");
        taskInput.setPrefWidth(400);
        taskInput.setStyle("-fx-font-size: 14px;");
        
        Button addButton = new Button("Add Task");
        addButton.setStyle("-fx-background-color: #4CAF50; -fx-text-fill: white;");
        
        Button clearCompletedButton = new Button("Clear Completed");
        clearCompletedButton.setStyle("-fx-background-color: #f44336; -fx-text-fill: white;");
        
        HBox inputBox = new HBox(10);
        inputBox.getChildren().addAll(taskInput, addButton, clearCompletedButton);
        inputBox.setPadding(new Insets(10));
        
        // Event handlers
        addButton.setOnAction(e -> addTask(taskInput));
        taskInput.setOnAction(e -> addTask(taskInput));
        
        clearCompletedButton.setOnAction(e -> {
            tasks.removeIf(Task::isCompleted);
        });
        
        // Filter event handlers
        allFilter.setOnAction(e -> filteredTasks.setPredicate(task -> true));
        activeFilter.setOnAction(e -> filteredTasks.setPredicate(task -> !task.isCompleted()));
        completedFilter.setOnAction(e -> filteredTasks.setPredicate(Task::isCompleted));
        
        // Layout
        VBox centerContent = new VBox(10);
        centerContent.getChildren().addAll(taskListView, inputBox);
        centerContent.setPadding(new Insets(10));
        root.setCenter(centerContent);
        
        // Status bar
        Label statusLabel = new Label();
        updateStatus(statusLabel);
        
        tasks.addListener((javafx.collections.ListChangeListener<Task>) c -> updateStatus(statusLabel));
        
        HBox statusBar = new HBox(statusLabel);
        statusBar.setPadding(new Insets(5));
        statusBar.setStyle("-fx-background-color: #f0f0f0;");
        root.setBottom(statusBar);
        
        // Add some sample tasks
        tasks.addAll(
            new Task("Complete JavaFX Todo App"),
            new Task("Add task filtering"),
            new Task("Implement task persistence"),
            new Task("Add due dates feature")
        );
        
        // Create scene
        Scene scene = new Scene(root, 700, 600);
        scene.getStylesheets().add(getClass().getResource("/styles.css").toExternalForm());
        primaryStage.setScene(scene);
        primaryStage.show();
        
        taskInput.requestFocus();
    }
    
    private void addTask(TextField taskInput) {
        String description = taskInput.getText().trim();
        if (!description.isEmpty()) {
            tasks.add(new Task(description));
            taskInput.clear();
        }
    }
    
    private void updateStatus(Label statusLabel) {
        long totalTasks = tasks.size();
        long completedTasks = tasks.stream().filter(Task::isCompleted).count();
        long activeTasks = totalTasks - completedTasks;
        
        statusLabel.setText(String.format("%d total | %d active | %d completed", 
                                        totalTasks, activeTasks, completedTasks));
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}