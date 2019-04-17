package TestModules;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

public class GroupPage {
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
		WebElement ctn_btn = wait.until(ExpectedConditions.elementToBeClickable(By.className("ZFr60d")));
		Actions actions = new Actions(driver);
		actions.moveToElement(ctn_btn).click().perform();
		WebElement token_input=wait.until(ExpectedConditions.elementToBeClickable(By.id("token-textbox")));
	    token_input.sendKeys("#########");
	    driver.findElement(By.id("continue-btn")).click();
		WebElement view = wait.until(ExpectedConditions.elementToBeClickable(By.className("btn")));
		view.click();
	}
	
	@Test
	public void TestGroupPage() {
		WebDriverWait wait = new WebDriverWait(driver,30);
		WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(By.id("btn-grp")));
		btn.click();
		Select preference = new Select(driver.findElement(By.id("sel1")));
		preference.selectByVisibleText("3");
		Select avoidance = new Select(driver.findElement(By.id("sel2")));
		avoidance.selectByVisibleText("3");
		Select size = new Select(driver.findElement(By.id("size")));
		size.selectByVisibleText("2");
		WebElement file_path = driver.findElement(By.id("file"));
		file_path.sendKeys("https://docs.google.com/spreadsheets/d/17ac0D1iDql0cnMIU7uxAUBPPaYDTkgNj1m1Pv7VFLWs/edit#gid=2061704772");
		WebElement create_grp_btn= driver.findElement(By.id("create-grp"));
		Actions actions= new Actions(driver);
		actions.moveToElement(create_grp_btn).click().perform();
		WebElement tab_1= driver.findElement(By.id("table1"));
		WebElement tab_2 = driver.findElement(By.id("table2"));
		assertEquals(true,(tab_1!=null&&tab_2!=null));
			
	}
	@After
		public void teardown() {
			driver.quit();
	}
}
