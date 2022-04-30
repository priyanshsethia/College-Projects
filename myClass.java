// Program to count steps taken by monkey to climb the tree.

// Importing of essential packages.
import java.io.*;
import java.util.*;
import java.lang.*;

public class myClass
{
	// StepsCounter() function to count steps.
	static void StepsCounter()
	{	
		// Using exception handling to avoid wrong input exception.
		try{	
			// Taking values from user.
			Scanner sc = new Scanner(System.in);
			System.out.print("\nEnter tree length : ");
			double N = sc.nextDouble();
			System.out.print("Enter jump length : ");
			double J = sc.nextDouble();
			System.out.print("Enter slip length : ");
			double S = sc.nextDouble();

			// Calculating steps.
			double steps = Math.ceil((double)(N-J)/(J-S));
			steps += (double)(N-steps*(J-S))/((double)J);
			System.out.println("\nSteps taken by monkey to reach at the top : " + steps);
			
		}
		catch(InputMismatchException e) {
			
			// Showing message & again calling StepsCounter() funtion.
			System.out.println("Invalid Input.");
			StepsCounter();	
		}	
	}	

	public static void main(String args[]) 
	{
		// Calling of function.
		StepsCounter();
	}
}