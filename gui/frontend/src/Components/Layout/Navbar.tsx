import { Container } from "react-bootstrap";
import { Navbar } from "react-bootstrap";

function Nav(props: any) {
  return (
    <Navbar variant="dark" style = {navStyle}>
      <Container>
        <Navbar.Brand href="/">Onyks_owl</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default Nav;


const navStyle = {
  backgroundColor: "#404040",
};