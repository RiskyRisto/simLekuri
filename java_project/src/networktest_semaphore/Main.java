package networktest_semaphore;

/*
 * Generic main program to activate a JavaSim process (here Network) playing the role of the actual main loop.
 */
public class Main {

	public static void main(String[] args) {

		Network m = new Network();

		m.Await();

		System.exit(0);
	}

}