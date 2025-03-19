import fitCvut from '../assets/fitcvut.svg'
import openDataLab from '../assets/opendatalab.svg'

export default function Footer() {
    return (
        <footer>
          <div className="p-2 mt-4 bg-light">
            <div className="row gx-3 align-items-center">
              <div className="col text-lg-start text-center">
                <p className="mb-0">
                    © 2025 Bc. Alexander Žibrita
                </p>
                <p className="mb-0">
                  Kontakt: <a href="mailto: zibriale@fit.cvut.cz">zibriale@fit.cvut.cz</a>
                </p>
                <p className="mb-0 fst-italic">
                  Provozovatel neodpovídá za správnost a úplnost zpracovaných dat a informací, ani tato
                  neověřuje a zříká se zodpovědnosti za veškeré škody a újmy, které by použitím těchto
                  dat mohly vzniknout.
                </p>
              </div>
              <div className="col-lg-auto text-center">
                <a href="https://fit.cvut.cz/" target="_blank" rel="noreferrer">
                  <img src={fitCvut} height="70px" width="200px" />
                </a>
                &nbsp;
                <a href="https://opendatalab.cz/" target="_blank" rel="noreferrer">
                  <img src={openDataLab} height="70px" width="100px" />
                </a>
              </div>
            </div>
          </div>
        </footer>
      )
}