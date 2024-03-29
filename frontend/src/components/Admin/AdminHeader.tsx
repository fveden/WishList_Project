import classNames from "classnames";
import styles from "./admin.module.css";
import React from "react";
import { Icon, IconButton } from "@chakra-ui/react";
import {
  HamburgerIcon
} from "@chakra-ui/icons";
import { FaUser } from "react-icons/fa";
import { IoExitSharp } from "react-icons/io5";
import { useNavigate } from "react-router-dom";
import { UserContext, UserContextType } from "../../context/UserContext";
interface IAdminHeader {
  toggleSideMenu: () => void;
}

function AdminHeader(props: IAdminHeader) {
  const { toggleSideMenu } = props;
  const { setAuthorizationTokens } =
    React.useContext(UserContext) as UserContextType;
  const [userScreenWidth, setUserScreenWidth] = React.useState(
    window.innerWidth
  );
  const navigate = useNavigate();
  React.useEffect(() => {
    window.addEventListener("resize", () => {
      setUserScreenWidth(window.innerWidth);
    });
  }, []);
  return (
    <header className={classNames(styles.header)}>
      <div className={styles.header_side}>
        {userScreenWidth <= 1050 && (
          <IconButton
            icon={<HamburgerIcon boxSize={6} color={"white"} />}
            _hover={{ background: "transparent" }}
            aria-label="Open side menu"
            w={"24px"}
            bg={"inherit"}
            onClick={toggleSideMenu}
          />
        )}
        <span
          className={classNames("page-text", "page-title-text", styles.logo)}
        >
          WISHLIST
        </span>
      </div>
      <div className={styles.header_side}>
        <Icon as={FaUser} boxSize={5} color={"white"} mr={1} />
        <p
          className={classNames("page-text", "page-reg-text", styles.username)}
        >
          Admin
        </p>
        <IconButton
          onClick={() => {
            setAuthorizationTokens(undefined, undefined);
            navigate("/");
          }}
          aria-label="Logout"
          w={"24px"}
          _hover={{ background: "transparent" }}
          bg={"inherit"}
          icon={<Icon as={IoExitSharp} boxSize={5} color={"white"} />}
        />
      </div>
    </header>
  );
}

export default AdminHeader;
