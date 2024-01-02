package exampleTest;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

import example.example;

public class exampleTest {

	example toy = new example();
	
	@Test //case1
	public void testCase1() {
		String string1 = toy.process("speak wordNone");
		assertEquals("speak *1*//wordNone recognized", string1);
	}
	
	@Test //case2
	public void testCase2() {
		String string2 = toy.process("wordNone");
		assertEquals("*1*//wordNone recognized", string2);
	}
	
	@Test //case3
	public void testCase3() {
		String string3 = toy.process("wordNonecontained");
		assertEquals("*1*contained//wordNone recognized", string3);
	}
	
	@Test //case4
	public void testCase4() {
		String string4 = toy.process("wwwwordNoneeee");
		assertEquals("www*1*eee//wordNone recognized", string4);
	}
	
	@Test //case5
	public void testCase5() {
		String string5 = toy.process("has wordNtwo");
		assertEquals("has *2*//wordNtwo recognized", string5);
	}
	
	@Test //case6
	public void testCase6() {
		String string6 = toy.process("wordNtwo");
		assertEquals("*2*//wordNtwo recognized", string6);
	}
	
	@Test //case7
	public void testCase7() {
		String string7 = toy.process("");
		assertEquals("//pass", string7);
	}
	
	@Test //case8
	public void testCase8() {
		String string8 = toy.process("midd*1*le");
		assertEquals("", string8);
	}
	
	@Test //case9
	public void testCase9() {
		String string9 = toy.process("*1*2*");
		assertEquals("", string9);
	}
	
	@Test //case10
	public void testCase10() {
		String string10 = toy.process("a normal sentence");
		assertEquals("a normal sentence//pass", string10);
	}
	
	@Test //case11
	public void testCase11() {
		String string11 = toy.process("wordnonewordNtw");
		assertEquals("wordnonewordNtw//pass", string11);
	}
	
	@Test //case12
	public void testCase12() {
		String string12 = toy.process("wordNone and wordNtwo");
		assertEquals("both pattern recognized", string12);
	}
}