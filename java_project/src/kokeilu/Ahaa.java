package kokeilu;

import java.io.IOException;
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Queue;

import org.javasim.streams.Draw;


public class Ahaa {
	private double x;
	public static double y;
	
	public Ahaa() {
	}

	public double getX() {
		return x;
	}
	
	public static void main(String[] args) throws ArithmeticException, IOException {
		Ahaa ahaa = new Ahaa();
		System.out.println(ahaa.getX());
		System.out.println(Ahaa.y);
		System.out.println(150427.60927045534 / 1050);
		
		Queue<Double> queue = new ArrayDeque<Double>();
		queue.offer(1.0);
		queue.offer(2.0);
		System.out.println(queue);
		System.out.println(queue.poll());
		System.out.println(queue);

		double[][] t = new double[3][5];
		for (int i = 0; i < t.length; i++) {
			for (int j = 0; j < t.length; j++) {
				t[i][j] = Math.random();
			}
		}

		Arrays.stream(t).map(e -> {
			return Arrays.toString(e);
		}).forEach(System.out::println);
		
		
//		try (var f = Files.newBufferedWriter(Paths.get("taulukko.txt"))) {
//			String s = Arrays.stream(t).map(e -> {
//				return Arrays.toString(e);
//			}).reduce((s1,s2) -> s1+ "\n" + s2).get();
//			f.write(s);
//		}
		
		Draw draw = new Draw(0.95);
		
		for (int i = 0; i < 10; i++) {
			System.out.println(draw.getBoolean());
		}
	}
}
