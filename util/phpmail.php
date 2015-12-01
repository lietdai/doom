<?php
require 'PHPMailer/PHPMailerAutoload.php';

class PhpMail {
    private  $_mailer;

    private $_sender;
    private $_password;
    private $_host;

    
    private static $_instance;
    private function __construct() {
        $this->_sender = "your email address";
        $this->_password = "your email password";
        $this->_mailer = new PHPMailer;
        $this->_mailer->isSMTP();
        $this->_mailer->Host = "smtp.exmail.qq.com";
        $this->_mailer->SMTPAuth = true;
        $this->_mailer->Username = $this->_sender;
        $this->_mailer->Password = $this->_password;
        $this->_mailer->SMTPSecure = 'tls';
        $this->_mailer->Port = '587';
        $this->_mailer->setFrom($this->_sender,"Robot");
        $this->_mailer->isHTML(true);            
        $this->_mailer->SMTPDebug = 3;                               // Enable verbose debug out
    }

    public static function getMailer(){
        if(!(self::$_instance instanceof self)){
            self::$_instance = new self;
        }
        return self::$_instance;
    }
    
    public function send($subject, $body, $mailto){

        $this->_mailer->addAddress($mailto);      
        $this->_mailer->Body = $body;
        $this->_mailer->Subject = $subject;        
        return $this->_mailer->send();
    }
    
    
}



//PhpMail::getMailer()->send("aaa","bbbb","root@1137.me");
