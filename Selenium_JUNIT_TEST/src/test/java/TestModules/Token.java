package TestModules;

import static org.junit.Assert.*;

import java.io.IOException;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class Token {
	WebDriver driver;
	String username;
	String password;
	@Before
	public void startBrowser() {
		System.setProperty("webdriver.chrome.driver", "C:\\driver\\chromedriver.exe");
	    driver= new ChromeDriver();
		driver.get("http://instructortool.us-east-2.elasticbeanstalk.com/");
		driver.findElement(By.id("login-btn")).click();
		WebElement userid=driver.findElement(By.id("identifierId"));
		userid.sendKeys("#######");
		userid.sendKeys(Keys.ENTER);
		WebDriverWait wait = new WebDriverWait(driver,30);
		WebElement asurite = wait.until(ExpectedConditions.elementToBeClickable(By.name("username")));
		asurite.sendKeys("######");
		WebElement pwd = wait.until(ExpectedConditions.elementToBeClickable((By.name("password"))));
		pwd.sendKeys("######");
		pwd.sendKeys(Keys.ENTER);
	}
	
	@Test
	public void ValidToken() throws IOException, InterruptedException{
		WebDriverWait wait = new WebDriverWait(driver,30);
		WebElement ctn_btn = wait.until(ExpectedConditions.elementToBeClickable(By.className("ZFr60d")));
		Actions actions = new Actions(driver);
		actions.moveToElement(ctn_btn).click().perform();
		String currentURL = driver.getCurrentUrl();
		Boolean result= currentURL.contains(currentURL);
		//assertEquals(true, result);
	    WebElement token_input=wait.until(ExpectedConditions.elementToBeClickable(By.id("token-textbox")));
	    token_input.sendKeys("########");
	    driver.findElement(By.id("continue-btn")).click();
	    assertEquals("http://instructortool.us-east-2.elasticbeanstalk.com/home", driver.getCurrentUrl());

	}
	@Test
	public void InvalidToken() {
		WebDriverWait wait = new WebDriverWait(driver,30);
		WebElement ctn_btn = wait.until(ExpectedConditions.elementToBeClickable(By.className("ZFr60d")));
		Actions actions = new Actions(driver);
		actions.moveToElement(ctn_btn).click().perform();
		WebElement token_input=wait.until(ExpectedConditions.elementToBeClickable(By.id("token-textbox")));
	    token_input.sendKeys("test");
	    driver.findElement(By.id("continue-btn")).click();
	    WebElement actual_results = wait.until(ExpectedConditions.presenceOfElementLocated(By.id("token-textbox")));
	    Boolean result = actual_results.equals(null);
	    assertEquals(false, result);
	}
	
	@After
	public void tearDown() {
		driver.close();
	}
}
