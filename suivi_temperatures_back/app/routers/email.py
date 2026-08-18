from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)


class EmailRequest(BaseModel):
    destinataire: EmailStr
    sujet: str
    corps: str


class EmailResponse(BaseModel):
    success: bool
    message: str | None = None
    error: str | None = None


def convertir_texte_en_html(texte: str) -> str:
    """
    Convertit un texte brut en HTML en remplaçant les newlines par <br>
    """
    texte_propre = texte.replace("\r", "").strip()
    html = texte_propre.replace("\n", "<br>")
    return html


async def envoyer_email(destinataire: str, sujet: str, corps: str) -> EmailResponse:
    """
    Envoie un email via SMTP Gmail
    
    Args:
        destinataire: Email de destination
        sujet: Sujet du mail
        corps: Corps du mail (texte brut, convertira en HTML automatiquement)
    
    Returns:
        EmailResponse avec succès ou erreur
    """
    try:
        # Nettoyage du texte
        texte_propre = corps.replace("\r", "").strip()
        contenu_html = convertir_texte_en_html(corps)
        
        logger.info(f"Envoi d'email à {destinataire} - Sujet: {sujet}")
        
        # Configuration du serveur SMTP
        serveur_smtp = smtplib.SMTP("smtp.gmail.com", 587)
        serveur_smtp.starttls()
        
        # Authentification
        serveur_smtp.login(settings.MAIL_USER, settings.MAIL_PASSWORD)
        
        # Création du message avec texte brut + HTML
        message = MIMEMultipart("alternative")
        message["Subject"] = sujet
        message["From"] = settings.MAIL_USER
        message["To"] = destinataire
        
        # Attach plain text version
        partie_texte = MIMEText(texte_propre, "plain", "utf-8")
        message.attach(partie_texte)
        
        # Attach HTML version
        partie_html = MIMEText(contenu_html, "html", "utf-8")
        message.attach(partie_html)
        
        # Envoi du mail
        serveur_smtp.sendmail(settings.MAIL_USER, destinataire, message.as_string())
        serveur_smtp.quit()
        
        logger.info(f"Email envoyé avec succès à {destinataire}")
        return EmailResponse(
            success=True,
            message="Email envoyé avec succès!"
        )
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = "Erreur d'authentification : vérifiez MAIL_USER et MAIL_PASSWORD"
        logger.error(f"{error_msg} - {str(e)}")
        return EmailResponse(
            success=False,
            error=error_msg
        )
    except smtplib.SMTPException as e:
        error_msg = f"Erreur SMTP : {str(e)}"
        logger.error(error_msg)
        return EmailResponse(
            success=False,
            error=error_msg
        )
    except Exception as e:
        error_msg = f"Erreur lors de l'envoi du mail : {str(e)}"
        logger.error(error_msg)
        return EmailResponse(
            success=False,
            error=error_msg
        )


@router.post("/envoyer", response_model=EmailResponse)
async def envoyer_mail(email_request: EmailRequest):
    """
    Route pour envoyer un email (texte brut converti en HTML)
    
    Body:
    {
        "destinataire": "user@example.com",
        "sujet": "Votre sujet",
        "corps": "Contenu du mail\navec plusieurs lignes"
    }
    
    Response:
    {
        "success": true,
        "message": "Email envoyé avec succès!"
    }
    """
    return await envoyer_email(
        email_request.destinataire,
        email_request.sujet,
        email_request.corps
    )
