package networktest;

public class Main {

	public static void main(String[] args) {
//	boolean isBreaks = false;

		for (int i = 0; i < args.length; i++) {
			if (args[i].equalsIgnoreCase("-help")) {
				System.out.println("Usage: Main [-breaks] [-help]");
				System.exit(0);
			}
//	    if (args[i].equalsIgnoreCase("-breaks"))
//		isBreaks = true;
		}

		Network m = new Network();

		m.Await();

		System.exit(0);
	}

}