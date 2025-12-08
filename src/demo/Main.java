import java.sql.Connection;

public class Main {
    public static void main(String[] args) {
        // Obtain the singleton instance of DatabaseConnection
        JDBC dbConnection = JDBC.getInstance();
        Connection connection = dbConnection.getConnection();
        
        // Check if the connection was successful
        if (connection != null) {
            System.out.println("Database connected successfully!");
        } else {
            System.out.println("Failed to connect to the database.");
        }
    }
}